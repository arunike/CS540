from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset and center it
def load_and_center_dataset(filename): 
    # Your implementation goes here!
    x = np.load(filename)
    mean = np.mean(x, axis = 0)
    
    return x-mean

# Get the covariance matrix
def get_covariance(dataset): 
    # Your implementation goes here!
    return np.dot(np.transpose(dataset), dataset) / (len(dataset) - 1)

# Get the first m eigenvectors and eigenvalues
def get_eig(S, m): 
    # Your implementation goes here!
    Lambda, U = eigh(S,subset_by_index = [len(S) - m, len(S) -1]) # Get the last m eigenvalues and eigenvectors
    Lambda = np.diag(np.sort(Lambda)[::-1]) # Sort the eigenvalues in descending order
    U = np.fliplr(U) # Sort the eigenvectors in descending order
    print(U)

    return Lambda,U

# Get the first m eigenvectors and eigenvalues
def get_eig_prop(S, prop): 
    # Your implementation goes here!
    Lambda, U = eigh(S) # Get the last m eigenvalues and eigenvectors
    i = sum(Lambda) * prop # Get the sum of the first i eigenvalues
    Lambda, U = eigh(S,subset_by_value = [i, np.inf]) # Get the eigenvalues and eigenvectors that sum to i
    Lambda = np.diag(np.sort(Lambda)[::-1]) # Sort the eigenvalues in descending order
    U = np.fliplr(U)
    
    return Lambda,U

# Project the image onto the eigenspace
def project_image(image, U): 
    # Your implementation goes here!
    projection = np.zeros(len(image)) # Initialize the projection vector
    
    for index in range(0,len(U[0])): # For each eigenvector
        projection += np.inner(U[:,index],image) * (U[:,index])
        
    return projection

# Display the original and projected image
def display_image(orig, proj): 
    # Your implementation goes here!

    # Reshape the images
    orig = orig.reshape(32,32).T 
    proj = proj.reshape(32,32).T 
    
    fig, (ax1,ax2) = plt.subplots(1, 2) # Create a figure with two subplots
    colorbar_1 = ax1.imshow(orig,aspect='equal') # Display the original image
    ax1.set_title('Original') # Set the title
    fig.colorbar(colorbar_1, ax = ax1,shrink = 0.55) # Add a colorbar
    colorbar_2 = ax2.imshow(proj,aspect = 'equal') # Display the projected image
    ax2.set_title('Projection') # Set the title
    fig.colorbar(colorbar_2, ax = ax2,shrink = 0.55) # Add a colorbar

    plt.show() # Display the figure

if __name__ == '__main__':
    def main():
        x = load_and_center_dataset('YaleB_32x32.npy')
        S = get_covariance(x)
        Lambda, U = get_eig(S, 2)
        projection = project_image(x[0], U)
        display_image(x[0], projection)

    main()