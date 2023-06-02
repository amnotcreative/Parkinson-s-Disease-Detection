import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.metrics import accuracy_score
from PIL import Image
import os

# Function to load spirals from folder and convert to numpy arrays
def load_spirals_from_folder(folder_path):
    spirals = []
    labels = []
    for label, label_folder in enumerate(os.listdir(folder_path)):
        label_folder_path = os.path.join(folder_path, label_folder)
        for filename in os.listdir(label_folder_path):
            image_path = os.path.join(label_folder_path, filename)
            image = Image.open(image_path).convert('L') # Convert to grayscale
            image = image.resize((50, 50)) # Resize to (50, 50) pixels
            spiral = np.array(image).flatten() # Flatten to 1D numpy array
            spirals.append(spiral)
            labels.append(label)
    return np.array(spirals), np.array(labels)

# Load training and testing spirals
train_path = 'D:/college/sem 8/project/dataset/spiral/training'
test_path = 'D:/college/sem 8/project/dataset/spiral/testing'
X_train, y_train = load_spirals_from_folder(train_path)
X_test, y_test = load_spirals_from_folder(test_path)

# Train SVM classifier
clf = svm.SVC(kernel='linear')
clf.fit(X_train, y_train)

# Test accuracy of trained classifier
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

example_image_path = 'sample.png'
image = Image.open(example_image_path).convert('L') # Convert to grayscale
image = image.resize((50, 50)) # Resize to (50, 50) pixels
example_spiral = np.array(image).flatten() # Flatten to 1D numpy array
example_spiral = example_spiral.reshape(50, 50)

# Predict if example spiral belongs to Parkinson's patient or healthy individual
prediction = clf.predict([example_spiral.flatten()])
if prediction == 1:
    print("This spiral belongs to a Parkinson's patient.")
else:
    print("This spiral belongs to a healthy individual.")

# Display the image sample used
plt.imshow(example_spiral, cmap='gray')
plt.show()