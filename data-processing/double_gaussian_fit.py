import os
import ROOT



# Defining a double Gaussian function
def double_gaussian(x, par):
    # par = [norm1, mean1, sigma1, norm2, mean2, sigma2]

    # Gaussian 1
    gauss1 = par[0] * ROOT.TMath.Gaus(x[0], par[1], par[2])

    # Gaussian 2
    gauss2 = par[3] * ROOT.TMath.Gaus(x[0], par[4], par[5])

    return gauss1 + gauss2

# Define an input file
input_files = [ #"/Users/leobailloeul/Documents/coding/formosa/data/processed/CA2967_1500V_rough1_tyvek.root" ,
               # "/Users/leobailloeul/Documents/coding/formosa/data/processed/CA2967_1500V_rough2_tyvek.root",
               # "/Users/leobailloeul/Documents/coding/formosa/data/processed/CA2967_1500V_rough3_tyvek.root",
               # "/Users/leobailloeul/Documents/coding/formosa/data/processed/CA2967_1500V_rough4_tyvek.root",
               # "/Users/leobailloeul/Documents/coding/formosa/data/processed/CA2967_1500V_rough5_tyvek.root",
               # "/Users/leobailloeul/Documents/coding/formosa/data/processed/CA2967_1500V_smooth1_tyvek.root" ,
               # "/Users/leobailloeul/Documents/coding/formosa/data/processed/CA2967_1500V_smooth2_tyvek.root",
               # "/Users/leobailloeul/Documents/coding/formosa/data/processed/CA2967_1500V_smooth3_tyvek.root",
               # "/Users/leobailloeul/Documents/coding/formosa/data/processed/CA2967_1500V_smooth4_tyvek.root",
               # "/Users/leobailloeul/Documents/coding/formosa/data/processed/CA2967_1500V_smooth5_tyvek.root"
               "/Users/leobailloeul/Documents/coding/formosa/data/processed/Source_testing_CA2967.root",
               "/Users/leobailloeul/Documents/coding/formosa/data/processed/Source_testing_CA3145.root",
               "/Users/leobailloeul/Documents/coding/formosa/data/processed/Source_testing_CA3191.root",
               "/Users/leobailloeul/Documents/coding/formosa/data/processed/Source_testing_CA3192.root",
               "/Users/leobailloeul/Documents/coding/formosa/data/processed/Source_testing_CA3205.root",
               "/Users/leobailloeul/Documents/coding/formosa/data/processed/Source_testing_CA3193.root"
               # Add more files as needed
               ]

output_name = "double_gaussian_output.root"
output_file = ROOT.TFile(output_name, "RECREATE")


# Create a canvas to store multiple histograms on
canvas = ROOT.TCanvas("canvas", "canvas", 1000, 1000)


sum = len(input_files)
a, b = sum//2, -(-sum//2)
canvas.Divide(a,b) # Store as many histograms as there are files 

# Defining histogram parameters
nBins = 100
minBin = 0
maxBin = 4000

# Loop over input files
for i, input_path in enumerate(input_files):
    
    # Open input file and get TTree object
    input_file = ROOT.TFile(input_path)
    tree = input_file.Get("Events")

    # Get "area_3046_4" branch and create TH1F object
    area_branch_name = "area_3046_4"
    area_branch = tree.GetBranch(area_branch_name)

    # Create histogram
    hist_name = f"run {i}"
    print(hist_name)
    hist = ROOT.TH1F(hist_name, hist_name, nBins, minBin, maxBin)
    tree.Project(hist_name, area_branch_name)

    # Fit histogram to single Gaussian function for first peak
    fit_func_peak_one = ROOT.TF1("fit_peak_one", "gaus", 0, 430)
    hist.Fit(fit_func_peak_one, "R")
   

    # Get the mean and std of the first peak
    peak_one_norm = fit_func_peak_one.GetParameter(0)
    peak_one_mean = fit_func_peak_one.GetParameter(1)
    peak_one_std = fit_func_peak_one.GetParameter(2)

    # Fit histogram for single Gaussian function for second peak
    fit_func_peak_two = ROOT.TF1("fit_peak_two", "gaus", 431, 3000)
    hist.Fit(fit_func_peak_two, "R+")

    # Get the mean and std for the second peak
    peak_two_norm = fit_func_peak_two.GetParameter(0)
    peak_two_mean = fit_func_peak_two.GetParameter(1)
    peak_two_std = fit_func_peak_two.GetParameter(2)

    # Fit the histogram to the double Gaussian function using the parameters given
    fit_func = ROOT.TF1("fit_func", double_gaussian, minBin, maxBin, 6)
    fit_func.SetParameters(peak_two_norm, peak_one_mean, peak_one_std, peak_two_norm, peak_two_mean, peak_two_std)
    # hist.Fit(fit_func, "R+")

    # Draw the histogram on the Canvas to the i-th pad
    canvas.cd(i) 
    # hist.Draw()
    fit_func_peak_one.Draw("Same")
    fit_func_peak_two.Draw("Same")
    
    # Write TH1F object(s) to output file
    output_file.cd()
    hist.Write()

    # Close the input file
    input_file.Close()
    
canvas.Update()


# Close output file
output_file.Close()