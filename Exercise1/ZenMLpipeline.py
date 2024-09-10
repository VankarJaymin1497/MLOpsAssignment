from zenml import step
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import optuna
from sklearn.model_selection import cross_val_score
from zenml import pipeline

@pipeline
def iris_pipeline(data_loader, train_models, optimize_models):
    X_train, X_test, y_train, y_test = data_loader()
    train_models(X_train, X_test, y_train, y_test)
    optimize_models(X_train, y_train)


#Data Loader Step
@step
def data_loader():
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test


#Model Training Step (Random Forest & SVM)
@step
def train_models(X_train, X_test, y_train, y_test):
    # Initialize MLFlow experiment
    mlflow.set_experiment("Iris_Classification_Comparison")
    
    def train_and_log_model(model_name, model, params):
        with mlflow.start_run(run_name=model_name):
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            mlflow.log_params(params)
            mlflow.log_metric("accuracy", accuracy)
            mlflow.sklearn.log_model(model, model_name + "_model")
            print(f"{model_name} Accuracy:", accuracy)
    
    # Train RandomForest
    rf_params = {"n_estimators": 100}
    rf_model = RandomForestClassifier(**rf_params)
    train_and_log_model("RandomForest", rf_model, rf_params)
    
    # Train SVM
    svm_params = {"kernel": "linear", "C": 1.0}
    svm_model = SVC(**svm_params)
    train_and_log_model("SVM", svm_model, svm_params)

#Hyperparameter Optimization Step (Optuna)
@step
def optimize_models(X_train, y_train):
    def optimize_model(trial, model_name):
        with mlflow.start_run(nested=True):
            if model_name == "RandomForest":
                n_estimators = trial.suggest_int("n_estimators", 50, 200)
                max_depth = trial.suggest_int("max_depth", 2, 32)
                rf_model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
                accuracy = cross_val_score(rf_model, X_train, y_train, cv=3, scoring="accuracy").mean()
                mlflow.log_param("model", model_name)
                mlflow.log_param("n_estimators", n_estimators)
                mlflow.log_param("max_depth", max_depth)
                mlflow.log_metric("cv_accuracy", accuracy)
                return accuracy
            elif model_name == "SVM":
                C = trial.suggest_float("C", 0.1, 10.0, log=True)
                kernel = trial.suggest_categorical("kernel", ["linear", "rbf", "poly"])
                svm_model = SVC(C=C, kernel=kernel)
                accuracy = cross_val_score(svm_model, X_train, y_train, cv=3, scoring="accuracy").mean()
                mlflow.log_param("model", model_name)
                mlflow.log_param("C", C)
                mlflow.log_param("kernel", kernel)
                mlflow.log_metric("cv_accuracy", accuracy)
                return accuracy
    
    def optimize_and_log_with_mlflow(model_name):
        mlflow.set_experiment(f"{model_name}_Hyperparameter_Optimization")
        with mlflow.start_run():
            study = optuna.create_study(direction="maximize")
            study.optimize(lambda trial: optimize_model(trial, model_name), n_trials=20)
            print(f"Best parameters for {model_name}: {study.best_params}")
            print(f"Best cross-validation accuracy for {model_name}: {study.best_value}")
    
    # Optimize both models
    optimize_and_log_with_mlflow("RandomForest")
    optimize_and_log_with_mlflow("SVM")

# Define the Pipeline
@pipeline
def iris_pipeline(data_loader, train_models, optimize_models):
    X_train, X_test, y_train, y_test = data_loader()
    train_models(X_train, X_test, y_train, y_test)
    optimize_models(X_train, y_train)

#Run the Pipeline
if __name__ == "__main__":
    
    # Create a pipeline instance
    pipeline_instance = iris_pipeline(
        data_loader=data_loader(),
        train_models=train_models(),
        optimize_models=optimize_models()
    )
    
    # Run the pipeline
    pipeline_instance.run()

