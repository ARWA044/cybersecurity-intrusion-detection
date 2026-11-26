import argparse
import pandas as pd
from pipeline import train_models

def main():
    parser = argparse.ArgumentParser(description="Train and evaluate the experimental IDS")
    parser.add_argument("csv", help="Path to an authorized labeled dataset")
    parser.add_argument("--no-autoencoder", action="store_true")
    args = parser.parse_args()
    data = pd.read_csv(args.csv, keep_default_na=False)
    print(pd.DataFrame(train_models(data, not args.no_autoencoder)["metrics"]).T.to_string())

if __name__ == "__main__":
    main()
