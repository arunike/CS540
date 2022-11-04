import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data
from torchvision import datasets, transforms

# Feel free to import other packages, if needed.
# As long as they are supported by CSL machines.

def get_data_loader(training = True):
    """
    TODO: implement this function.

    INPUT: 
        An optional boolean argument (default value is True for training dataset)

    RETURNS:
        Dataloader for the training set (if training = True) or the test set (if training = False)
    """

    custom_transform = transforms.Compose([ ## Compose a list of transforms
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    train_set = datasets.FashionMNIST('./data', train = True, download = True, transform = custom_transform) ## Create a train set dataset object
    test_set = datasets.FashionMNIST('./data', train = False, transform = custom_transform) ## Create a test set dataset object
    
    if training == True: ## If training is True, return the training set
        trainLoader = torch.utils.data.DataLoader(train_set, batch_size = 64) 
    else: ## If training is False, return the test set
        trainLoader = torch.utils.data.DataLoader(test_set, batch_size = 64, shuffle = False)
    
    return trainLoader

def build_model():
    """
    TODO: implement this function.

    INPUT: 
        None

    RETURNS:
        An untrained neural network model
    """

    model = nn.Sequential(nn.Flatten(), nn.Linear(28 * 28, 128), nn.ReLU(), nn.Linear(128, 64), nn.ReLU(), nn.Linear(64, 10)) ## Add the fully connected layers

    return model

def train_model(model, train_loader, criterion, T):
    """
    TODO: implement this function.

    INPUT: 
        model - the model produced by the previous function
        train_loader  - the train DataLoader produced by the first function
        criterion   - cross-entropy 
        T - number of epochs for training

    RETURNS:
        None
    """

    criterion = nn.CrossEntropyLoss() ## Implement the training procedure
    opt = optim.SGD(model.parameters(), lr = 0.001, momentum = 0.9) ## Create a optimizer for the model
    model.train() ## Set model to training

    for epochs in range(T): ## Loop over the training data
        ## Variable initialization 
        running_loss = 0.0 
        correct = 0
        total = 0 
        count = 0

        for i, data in enumerate(train_loader, 0): ## Loop over the batches using enumeration 
            inputs, labels = data ## Obtain the data 
            opt.zero_grad() ## Clear the parameter gradients
            outputs = model(inputs) ## Forward pass
            loss = criterion(outputs, labels) ## Compute the loss
            loss.backward() ## Backward pass
            opt.step() ## Update the parameters based on the gradients
            _, predicted = torch.max(outputs.data, 1) ## Obtain the predicted labels
            correct += (predicted == labels).sum().item() ## Update the number of correct predictions
            running_loss += loss.item() ## Update the loss
            total += labels.size(0) ## Update the total number of labels
            count += 1 ## Update the count

        print('Train Epoch: '+ str(epochs) + ' Accuracy: ' + str(correct) + '/' + str(total) + '(' + '{:.2f}'.format(100 * (correct / total)) + '%' + ') Loss: ' + '{:.3f}'.format(running_loss / count)) ## Print the output of the model 


def evaluate_model(model, test_loader, criterion, show_loss = True):
    """
    TODO: implement this function.

    INPUT: 
        model - the the trained model produced by the previous function
        test_loader    - the test DataLoader
        criterion   - copy-entropy 

    RETURNS:
        None
    """

    criterion = nn.CrossEntropyLoss() ## Implement the training procedure
    model.eval() ## Turn model into evaluation mode

    ## Variable initialization
    running_loss = 0.0 
    correct = 0
    total = 0
    count = 0

    with torch.no_grad(): ## Disable gradient calculation
        for data, labels in test_loader: ## Loop over the batches
            outputs = model(data) ## Forward pass
            _, predicted = torch.max(outputs.data, 1) ## Obtain the predicted labels
            loss = criterion(outputs, labels) ## Compute the loss
            running_loss += loss.item() ## Update the loss
            count = count + 1 ## Update the count
            total += labels.size(0) ## Update the total number of labels
            correct += (predicted == labels).sum().item() ## Update the number of correct predictions
        
        if show_loss == True: ## If show_loss is True, print the loss
            print_out = 'Average loss: ' + '{:.4f}'.format(running_loss / count) + '\nAccuracy: ' + '{:.2f}'.format(100 * (correct / total)) + '%' 
        else: ## If show_loss is False, do not print the loss
            print_out = 'Accuracy: ' + '{:.2f}'.format(100 * (correct / total)) + '%' 

        print(print_out)

def predict_label(model, test_images, index):
    """
    TODO: implement this function.

    INPUT: 
        model - the trained model
        test_images   -  test image set of shape Nx1x28x28
        index   -  specific index  i of the image to be tested: 0 <= i <= N - 1

    RETURNS:
        None
    """

    class_names = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankle Boot"] ## List of class names
    logits = model(test_images[index]) ## Obtain the logits
    prob = F.softmax(logits, dim = 1) * 100 ## Obtain the probabilities
    values, indices = torch.topk(prob, 3) ## Obtain the top 3 probabilities and their indices
    
    for i in range(3): ## Loop over the top 3 probabilities
        print(str(class_names[indices[0][i]]) + ": " + str(round(values[0][i].item(), 2)) + "%" )

if __name__ == '__main__':
    '''
    Feel free to write your own test code here to examine the correctness of your functions. 
    Note that this part will not be graded.
    '''

    criterion = nn.CrossEntropyLoss()
    train_loader = get_data_loader()
    test_loader = get_data_loader(training=False)

    print(type(train_loader))
    print(train_loader.dataset)
    
    model = build_model()
    train_model(model, train_loader, criterion, 5)
    evaluate_model(model, test_loader, criterion, show_loss = True)
    pred_set, _ = next(iter(test_loader))
    predict_label(model, pred_set, 4)