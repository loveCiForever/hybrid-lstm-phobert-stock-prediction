# src/matching_parsing/main.py

from src.matching_parsing.runner import run
import pandas as pd


if __name__ == "__main__":
    parsed_context = run()
    parsed_context.to_csv("data/parsed/dataset.csv", index=False)