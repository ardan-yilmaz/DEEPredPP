import numpy as np
import torch
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, matthews_corrcoef
from utils import custom_mcc

class ModelEvaluator:
    def __init__(self, model, thresholds, device='cpu'):
        """
        Initialize the ModelEvaluator class with the trained model and optimal thresholds.
        :param model: Trained PyTorch model.
        :param thresholds: Optimal thresholds for each class determined by ThresholdFinder.
        :param device: Computation device ('cpu' or 'cuda').
        """
        self.model = model
        self.thresholds = thresholds
        self.device = device

    def evaluate(self, loader):
        """
        Evaluates the model on the given dataset with the specified thresholds.
        :param loader: DataLoader for the dataset.
        :return: Dictionary of evaluation metrics.
        """ 
        true_labels_list = []
        predictions_list = []

        self.model.eval()
        with torch.no_grad():
            for _, inputs, targets in loader:
                inputs, labels = inputs.to(self.device), targets.to(self.device)
                outputs = torch.sigmoid(self.model(inputs))

                preds = outputs > torch.Tensor(self.thresholds).to(self.device)
                
                true_labels_list.append(labels.cpu().numpy())
                predictions_list.append(preds.cpu().numpy())

        true_labels = np.vstack(true_labels_list)
        predictions = np.vstack(predictions_list)

        metrics = self.calculate_metrics(true_labels, predictions)
        return metrics

    @staticmethod
    def calculate_metrics(true_labels, predictions):
        """
        Calculates and returns the evaluation metrics.
        :param true_labels: Numpy array of true labels.
        :param predictions: Numpy array of predictions.
        :return: Dictionary of evaluation metrics including accuracy, precision, recall, F1-score, MCC, and counts of TP, FP, FN, TN per class.
        """
        # Calculate metrics
        precision, recall, f1, _ = precision_recall_fscore_support(true_labels, predictions, average='micro')
        mcc = custom_mcc(true_labels.ravel(), predictions.ravel())
        
        # Initialize counters
        TP = FP = FN = TN = 0
        
        # Calculate TP, FP, FN, TN for each class
        for i in range(predictions.shape[1]):  # Iterate through each class
            tp = np.sum((predictions[:, i] == 1) & (true_labels[:, i] == 1))
            fp = np.sum((predictions[:, i] == 1) & (true_labels[:, i] == 0))
            fn = np.sum((predictions[:, i] == 0) & (true_labels[:, i] == 1))
            tn = np.sum((predictions[:, i] == 0) & (true_labels[:, i] == 0))
            
            TP += tp
            FP += fp
            FN += fn
            TN += tn
        
        # Calculate accuracy manually as a sanity check
        total_samples = true_labels.size
        accuracy = (TP + TN) / total_samples if total_samples else 0
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'F1-score': f1,
            'MCC': mcc,
            'TP': TP,
            'FP': FP,
            'FN': FN,
            'TN': TN
        }




# evaluator = ModelEvaluator(best_model, optimal_thresholds, device='cuda' if torch.cuda.is_available() else 'cpu')
# evaluation_metrics = evaluator.evaluate(eval_loader)

# print("Evaluation Metrics:", evaluation_metrics)
