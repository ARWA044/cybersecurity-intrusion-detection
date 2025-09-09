# 🛡️ Cybersecurity Intrusion Detection System

A comprehensive machine learning-based intrusion detection system built with Python and Streamlit. This system uses multiple ML algorithms to detect potential security threats in network traffic and user behavior.

## 🚀 Features

- **Multiple ML Models**: Random Forest, XGBoost, Logistic Regression, and Autoencoder
- **Real-time Detection**: Test new data for potential intrusions
- **Interactive Dashboard**: User-friendly Streamlit interface
- **Model Performance Analysis**: Compare different models' effectiveness
- **Data Visualization**: Charts and graphs for better understanding

## 📊 Model Performance

The system includes four different machine learning models:

- **Random Forest**: Ensemble method for robust classification
- **XGBoost**: Gradient boosting for high accuracy
- **Logistic Regression**: Linear model for interpretability
- **Autoencoder**: Deep learning for anomaly detection

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cybersecurity-intrusion-detection.git
   cd cybersecurity-intrusion-detection
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_dashboard.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 📁 Project Structure

```
cybersecurity-intrusion-detection/
├── streamlit_dashboard.py          # Main Streamlit application
├── data_processing.py              # Data loading and cleaning
├── feature_engineering.py          # Feature creation and scaling
├── model_training.py               # ML model training functions
├── evaluation.py                   # Model evaluation metrics
├── autoencoder_model.py            # Autoencoder implementation
├── security_rules.py               # Security rule definitions
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── .gitignore                      # Git ignore file
└── LICENSE                         # MIT License
```

## 🔍 Usage

### Dashboard Overview
- **System Status**: View overall security metrics
- **Attack Distribution**: See normal vs attack data distribution
- **Model Performance**: Quick overview of model accuracy

### Testing New Data
1. Navigate to "Test New Data" page
2. Fill in the network and security features:
   - Network Packet Size
   - Session Duration
   - Login Attempts
   - Failed Logins
   - Unusual Time Access
   - Protocol Type
   - Encryption Used
   - Browser Type
   - IP Reputation Score
3. Click "Detect Intrusion"
4. View results from all four models

### Model Performance
- Compare accuracy, precision, recall, and F1-score
- View confusion matrices
- Analyze model effectiveness

## 📊 Dataset

The system uses a cybersecurity intrusion detection dataset with the following features:

- **Network Features**: Packet size, session duration, protocol type
- **Security Features**: Login attempts, failed logins, encryption type
- **Behavioral Features**: Unusual time access, IP reputation, browser type

## 🧠 Machine Learning Pipeline

1. **Data Preprocessing**: Cleaning and encoding categorical variables
2. **Feature Engineering**: Creating custom features and scaling
3. **Data Balancing**: Using SMOTE for handling class imbalance
4. **Model Training**: Training multiple ML algorithms
5. **Evaluation**: Comprehensive performance metrics
6. **Prediction**: Real-time intrusion detection

## 🔧 Configuration

The system can be configured through the Streamlit interface:

- **Model Parameters**: Adjust Random Forest and XGBoost settings
- **Detection Thresholds**: Modify sensitivity levels
- **Data Processing**: Enable/disable balancing and scaling

## 📈 Performance Metrics

The system provides comprehensive evaluation metrics:

- **Accuracy**: Overall correctness of predictions
- **Precision**: True positive rate
- **Recall**: Sensitivity to attacks
- **F1-Score**: Harmonic mean of precision and recall
- **ROC-AUC**: Area under the ROC curve

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Dataset: Cybersecurity Intrusion Detection Dataset
- Libraries: Streamlit, Scikit-learn, XGBoost, TensorFlow
- Community: Open source machine learning community

## 📞 Support

If you have any questions or need help with the project, please:

1. Check the [Issues](https://github.com/yourusername/cybersecurity-intrusion-detection/issues) page
2. Create a new issue if your problem isn't already addressed
3. Contact the maintainers

## 🔮 Future Enhancements

- [ ] Real-time data streaming integration
- [ ] Additional ML models (SVM, Neural Networks)
- [ ] Advanced visualization features
- [ ] API endpoints for external integration
- [ ] Docker containerization
- [ ] Cloud deployment options

---

**Built with ❤️ for cybersecurity professionals**
