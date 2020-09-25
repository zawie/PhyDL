from torch.utils.data import Dataset
import numpy as np
import torch
import os

from transformations import transformSequences

def getLatestInt():
    latestInt = 0
    for filename in os.listdir("data"):
        if filename.endswith(".npy"):
            numeric_tag = ""
            for char in filename:
                if char.isdigit():
                    numeric_tag += char
            num = int(numeric_tag)
            if num > latestInt:
                latestInt = num
    return latestInt

def getDataSets(int_tag=-1):
    """
    1. Reads path files
    2. Forms SimpleDataset class
    3. Returns train, dev, test datasets in dictionary format
        {"train":trainSet, "dev":devSet, "test":testSet}
    """
    if int_tag < 0:
        int_tag = getLatestInt()
    dataPath = f"data/recombination_data{int_tag}.npy"
    labelsPath = f"data/recombination_labels{int_tag}.npy"

    data = np.load(dataPath)
    labels = np.load(labelsPath)

    X_Data = data.tolist()
    Y_Data = labels.tolist()

    initialDataSet = SimpleDataset(X_Data, Y_Data)

    trainSet, devSet, testSet = initialDataSet.formDatasets()

    datasets = {"train":trainSet, "dev":devSet, "test":testSet}

    return datasets

class SimpleDataset(Dataset):
    def __init__(self, data, labels, doTransform=False):
        """
        Initializes the Dataset.
        This primarily entiles reading the generated sequeences into a python list

        Input:
        data - list of quartet sequeences
        labels - list of corresponding labesl
        """
        #Validate input
        assert len(data) == len(labels)
        #Create data fields
        self.X_data = []
        self.Y_data = []

        if doTransform:
            #Transform data
            for datapoint in zip(data,labels):
                (sequences,label) = datapoint
                (transX,transY) = transformSequences(sequences,label)
                self.X_data += transX
                self.Y_data += transY
        else:
            self.X_data = data
            self.Y_data = labels

        #Validate output
        assert len(self.X_data) == len(self.Y_data)

    def __getitem__(self, index):
        """
        Gets a certain tree across all three trees (alpha,beta,charlie)
        """
        return self.X_data[index], self.Y_data[index]

    def getData(self):
        """
        Gets class instances data and labels
        """
        return self.X_data, self.Y_data

    def __len__(self):
        """
        Returns the number of entries in this dataset
        """
        return len(self.X_data)

    def __add__(self, other):
        """
        Merges to datasets
        """
        return SimpleDataset(self.X_data+other.X_data, self.Y_data+other.Y_data, doTransform=False)

    def formDatasets(self, setProbabilities = [100, 0, 0]):
        """
        Forms SimpleDataset class datasets with the correct probabilities

        Input:
        setProbabilities - list of probabilities: [trainProb, devProb, testProb]

        Output:
        newSets - [trainSet, devSet, testSet]
        """
        assert sum(setProbabilities) == 100 #is a probability distribution

        numAllDatapoints = len(self.Y_data)
        newSets = []
        indexCounter = 0
        for setProbability in setProbabilities:
            numDatapoints = int(setProbability/100 * numAllDatapoints)
            print(numDatapoints)

            #check for mutation??
            newData = self.X_data[indexCounter:indexCounter+numDatapoints]
            newLabels = self.Y_data[indexCounter:indexCounter+numDatapoints]

            newSet = SimpleDataset(torch.tensor(newData,dtype=torch.float),
                                   torch.tensor(newLabels, dtype=torch.long))
            newSets.append(newSet)

            indexCounter += numDatapoints

        return tuple(newSets)

    def saveData(self, pathPrefix):
        """
        Saves the datasets data and labels
        """
        np.save(pathPrefix + "_data", self.X_data)
        np.save(pathPrefix + "_labels", self.Y_data)


# if __name__ == "__main__":
#     dataPath = "/Users/rhuck/Downloads/DL_Phylogeny/Recombination/dataClassData/recombination_data0.npy"
#     labelsPath = "/Users/rhuck/Downloads/DL_Phylogeny/Recombination/dataClassData/recombination_labels0.npy"


#     X_data = np.load(dataPath, allow_pickle=True)
#     Y_data = np.load(labelsPath, allow_pickle=True)
#     data = X_data.tolist()
#     labels = Y_data.tolist()
#     dataset = SimpleDataset(data, labels)
#     data, labels = dataset.getData()
#     print("data: ", data)
#     print("labels: ", labels)
#     print("length: ", len(dataset))

#     print("=======================\n")
#     (trainSet, devSet, testSet) = dataset.formDatasets()
#     print("training set: ", trainSet.getData())
#     print("dev set: ", devSet.getData())
#     print("test set: ", testSet.getData())
