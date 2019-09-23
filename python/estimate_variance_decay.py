import netCDF4
import numpy as np
import plot_info
import matplotlib.pyplot as plt
import sys


def speedup_mlmc(variances, levels, work):

    # We assume we use 10 000 samples on the finest level for MC
    # and find the work for MLMC using said error tolerance
    Mbase = 10000
    workBase = work[-1]*Mbase
    errorMCBase = variances[-1]/Mbase

    maxLevel = len(variances)

    bestConfiguration = {'L':0,
                         'M': [Mbase],
                         'Speedup' : 1,
                         'variance' : max(variances),
                         'work' : [work[-1]],
                         'sigma2':[variances[-1]],
                         'workBase' : workBase,
                         'error': errorMCBase}

    for L in range(1, maxLevel):
        sigmas2 = np.zeros(L+1)
        sigmas2[0] = variances[-L-1]
        sigmas2[1:] = levels[-L:]
        workLocal = work[-L-1:]
        sumSigmaWork = np.sum(np.sqrt(sigmas2*workLocal))
        M = np.zeros(L+1)
        M = 1.0/errorMCBase * (np.sqrt(sigmas2/workLocal))*sumSigmaWork
        M = np.ceil(M)
        workConfiguration = np.sum(M*workLocal) + np.sum(M[1:]*workLocal[:-1])
        speedup = workBase/workConfiguration

        errorMLMC = np.sum(sigmas2/M)


        # We actually get some floating point errors, therefore, we need to adjust our expectations a bit
        epsilon = 10*max(errorMCBase*(np.finfo(type(errorMCBase)).eps), errorMLMC*np.finfo(type(errorMCBase)).eps)

        if  errorMLMC > errorMCBase + epsilon:
            raise Exception("MLMC could not match MC error, MLMC_Error=%s, MC_error=%s" %
                            (np.float64(errorMLMC), np.float64(errorMCBase)))



        if speedup > bestConfiguration['Speedup']:
            bestConfiguration = {'L' : L,
                                 'M':M,
                                 'Speedup':speedup,
                                'variance':max(variances),
                                 'work' : workLocal,
                                 'sigma2':sigmas2,
                                 'workBase' : workBase,
                                  'error': errorMCBase}


    return bestConfiguration


def compute_speedup(resolutions, variance_single_level, variance_multilevel):
    resolutions = np.array(resolutions)
    
    work = resolutions**2
    
    best_speedup = speedup_mlmc(variance_single_level, variance_multilevel, work)
    
    
    return best_speedup['Speedup']
    

def load(filename, variable):
    samples = []
    
    if variable == 'all':
        variables = ['rho', 'mx', 'my', 'E']
    else:
        variables = [variable]
    
    with netCDF4.Dataset(filename) as f:
        for attr in f.ncattrs():
            plot_info.add_additional_plot_parameters(filename.replace("/", "_") + "_" + attr, f.getncattr(attr))
        
        sample = 0
        shape = f.variables['sample_0_rho'][:,:,0].shape
        next_sample_to_print = 1
        while f'sample_{sample}_rho' in f.variables.keys():
            if sample % 80 > next_sample_to_print:
                sys.stdout.write("#")
                sys.stdout.flush()
                next_sample_to_print += 1
            
            data = np.zeros((*shape, len(variables)))
            for n, variable in enumerate(variables):
                key = f'sample_{sample}'
                data[:,:,n] = f.variables[key][:,:,0]
            samples.append(data)
            sample += 1
                
    print()
    return np.array(samples)


def get_line_integral(d):
    
    for h in range(1,len(d)):
        d[h] += d[h-1]
    for h in range(1,len(d)):
        d[h] /=(2*h+1)**2
        #d[h] /= 4*(2*h+1)
        
    return d
    

def load_structure(filename, variable, p):
    print(filename)
    samples = []
    
    if variable == 'all':
        variables = ['rho', 'mx', 'my', 'E']
    else:
        variables = [variable]
    
    with netCDF4.Dataset(filename) as f:
        for attr in f.ncattrs():
            plot_info.add_additional_plot_parameters(filename.replace("/", "_") + "_" + attr, f.getncattr(attr))
        
        sample = 0
        shape = f.variables['sample_0_rho'][:,:,0].shape
        next_sample_to_print = 1
        while f'sample_{sample}_rho' in f.variables.keys():
            if sample % 80 > next_sample_to_print:
                sys.stdout.write("#")
                sys.stdout.flush()
                next_sample_to_print += 1
            
            data = np.zeros((shape[0]))
            for n, variable in enumerate(variables):
                key = f'sample_{sample}'
                data[:] += get_line_integral(f.variables[key][:,0,0])
            data = data**(1/p)
            samples.append(data)
            sample += 1
                
    print()
    return np.array(samples)


def compute_variance_decay(resolutions, computer, norm_ord):
    variances = []
    variances_details = []
    
    for resolution in resolutions:
        print(f"Resolution: {resolution}")
        data = computer(resolution)
        variance_single_level = np.linalg.norm(np.var(data, axis=0).flatten(), ord=norm_ord)/float(resolution)**(1/norm_ord)
        
        variances.append(variance_single_level)
        if resolution > resolutions[0]:
            detail = data - data_coarse
            
            variance_detail = np.linalg.norm(np.var(detail, axis=0).flatten(), ord=norm_ord)/float(resolution)**(1/norm_ord)
            
            
            variances_details.append(variance_detail)
        if resolution < resolutions[-1]:
            data_coarse = np.repeat(data, 2, 1)
            
    return variances, variances_details


def plot_variance_decay(title, resolutions, sample_computer, norm_ord, name):
    variances, variances_details = compute_variance_decay(resolutions, 
                                                                    sample_computer,
                                                                    norm_ord)
    
    
    speedups = [1]
    
    for n in range(1, len(resolutions)):
        local_resolutions = resolutions[:n+1]
        
        # Notice the max, Monte Carlo is always a form of MLMC, so we 
        # have a minimum speedup of one!
        speedup = max(1, compute_speedup(local_resolutions, 
                                  variances[:n+1],
                                  variances_details[:n]))
        
        speedups.append(speedup)
        
        
    fig, ax1 = plt.subplots()
    ax1.loglog(resolutions, variances, '-o', 
               label=f'$||\\mathrm{{Var}}({name.format(N="N")})||_{{L^{{{norm_ord}}}}}$')
    
    
    ax1.loglog(resolutions[1:], variances_details, '-*', 
               label=f'$||\\mathrm{{Var}}({name.format(N="N")}-{name.format(N="N/2")})||_{{L^{{{norm_ord}}}}}$',
               basex=2, basey=2)
    
    ax1.legend()
    
    ax1.set_xlabel("Resolution ($N$)")
    
    ax1.set_ylabel("Variance")
    
    plt.xticks(resolutions, [f'${r}$' for r in resolutions])
    
    #plt.title(f'Structure function variance decay\n{title}\nVariable: {variable}')
    
    plot_info.savePlot(f'variance_decay_{name}_{norm_ord}_{title}')
    
    plot_info.saveData(f'variance_details_{name}_{norm_ord}_{title}', variances_details)

    plot_info.saveData(f'variance_{name}_{norm_ord}_{title}', variances)
    
    plot_info.saveData(f'variance_decay_resolutions_{name}_{norm_ord}_{title}', resolutions)
    
    ax2 = ax1.twinx()

    
    
    ax2.plot(resolutions, speedups, '--x', label='MLMC Speedup')

    
    ax2.legend(loc=1)

    ax2.set_xscale("log", basex=2)
    ax2.set_xticks(resolutions, [f'${r}$' for r in resolutions])
    ax2.set_ylabel("Potential MLMC speedup")
            
    ylims = ax2.get_ylim()
    
    ax2.set_ylim([min(ylims[0], 0.5), max(ylims[1], 3)])
    plt.xticks(resolutions, [f'${r}$' for r in resolutions])
    
    plot_info.savePlot(f'variance_decay_with_speedup_{name}_{norm_ord}_{title}')
    
    plot_info.saveData(f'variance_decay_speedups_{name}_{norm_ord}_{title}', speedups)
     
