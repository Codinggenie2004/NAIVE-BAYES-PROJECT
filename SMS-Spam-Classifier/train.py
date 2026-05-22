"""
SMS Spam Classifier — Model Pre-Training Script
Runs training and serializes model/vectorizer artifacts to disk.
"""

import os
import sys

# Ensure the module can find imports relative to this script
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from model import train_model

def main():
    print("⏳ Starting model training and serialization...")
    try:
        stats = train_model()
        print("✅ Model trained and serialized successfully!")
        print(f"📊 Accuracy: {stats['accuracy']}%")
        print(f"📊 Precision: {stats['precision']}%")
        print(f"📊 Recall: {stats['recall']}%")
        print(f"📊 Vocabulary Size: {stats['vocab_size']}")
    except Exception as e:
        print(f"❌ Error during training: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
