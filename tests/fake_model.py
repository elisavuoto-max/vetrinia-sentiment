class FakeSentimentModel:
    def predict(self, texts):
        results = []
        for text in texts:
            value = text.lower()
            if "amazing" in value or "love" in value or "great" in value:
                results.append("positive")
            elif "bad" in value or "terrible" in value or "hate" in value:
                results.append("negative")
            else:
                results.append("neutral")
        return results

    def predict_proba(self, texts):
        probabilities = []
        for text in texts:
            value = text.lower()
            if "amazing" in value or "love" in value or "great" in value:
                probabilities.append([0.02, 0.03, 0.95])
            elif "bad" in value or "terrible" in value or "hate" in value:
                probabilities.append([0.94, 0.04, 0.02])
            else:
                probabilities.append([0.10, 0.82, 0.08])
        return probabilities
