from pathlib import Path


class FeatureExtractor:
    def __init__(self):
        # default constructor
        self.extractor_name = self.__class__.__name__  # something unique


class SimpleExtractor(FeatureExtractor):
    def analyze_body(self, text, **context):
        return True
        # I don't even care about the context (like a dictionary)
        # return {
        #     "I am very smart": False,
        #     "features": {
        #         "finding": "dog" in text.lower()
        #     }
        # }


class HandTunedExtractor(FeatureExtractor):
    def analyze_body(self, text, **context):
        return True
        # I don't even care about the context
        # return {
        #     "version": "2.0",
        #     "features": {
        #         "finding": "dog" in text.lower() and not "dawg" in text.lower()
        #     }
        # }


class VerySophisticatedExtractor(FeatureExtractor):
    def __init__(self, local_state_path):
        # I have a slow startup
        local_state_path = Path(local_state_path)  # turn a string into a path Python can use
        self.extractor_name = "{}/{}".format(self.__class__.__name__, local_state_path)
        super().__init__()  # calls the ancestral .__init__ of FeatureExtractor above
        self.data = local_state_path.read_bytes()

    def analyze_body(self, text, publication_date=None, **context):
        # I do use some context
        if publication_date.year > 2022:
            raise ValueError("This article is from the future")
            # execution would stop here
        return {
            "git-commit": "cafebee",
            **some_big_third_party_GPU_miner.extract_keywords(
                text.decode(),
                massive_other_stuff=self.data,
                whole_buncha_contaxt=context,
            ),
        }


def combine_feature_extractors(text):
    results = {}
    for fx in [
        SimpleExtractor(),
        HandTunedExtractor(),
        VerySophisticatedExtractor("/some/ML/data/here"),
        VerySophisticatedExtractor("/some/different/ML/data/here"),
        VerySophisticatedExtractor("/you/can/keep/going/with/more/data"),
    ]:
        try:
            results[fx.extractor_name] = fx.analyze_body(text, publication_date=2022, timeout=100.)
        except Exception as e:
            results[fx.extractor_name] = {"error": str(e)}
    # up to you to jam the results together in an intelligent way - maybe pruning the dictionary result
    return results  # or not