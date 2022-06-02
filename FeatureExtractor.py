from collections import Counter
from os import PathLike
from typing import Iterable, Optional


class FeatureExtractor:
    def __init__(self):
        # default constructor
        self.extractor_name = self.__class__.__name__  # something unique


# In practice, this class is more interesting than the others below.
class WordFrequencyExtractor(FeatureExtractor):
    def analyze_body(self, text: str, **context):
        # I don't even care about the context
        word_frequencies = Counter(w.lower() for w in text.split())  # loops through only once
        return {
            "features": {
                "n_unique_words": len(word_frequencies),
                "matches": word_frequencies,
            }
        }


class HandTunedExtractor(FeatureExtractor):
    keywords = {"dog", "dogs"}  # This is a class member. It is the same for all instances

    def analyze_body(self, text: str, **context):
        # I don't even care about the context
        words = [w.lower() for w in text.split()]
        return {
            "features": {
                "matches": {k: k in words for k in self.keywords},
                "n_total_words": len(words),
            }
        }


class MoreGenericExtractor(FeatureExtractor):
    def __init__(self, keywords: Iterable):
        super().__init__()
        self.keywords = keywords  # This is an instance member. Each instance maintains its own.

    # Notice how this method is identical to the one above? Maybe I could have written the generic one first
    def analyze_body(self, text, **context):
        # I don't even care about the context
        words = [w.lower() for w in text.split()]
        return {
            "features": {
                "matches": {k: k in words for k in self.keywords},
                "n_total_words": len(words),
            }
        }


# Notice the inheritance here
class EvenMoreGenericExtractor(MoreGenericExtractor):
    # instead of initializing with a list of keywords, I load those from a file
    def __init__(self, filename: PathLike):
        super().__init__()
        self.keywords = filename.read_text().split()  # Instance member

    # And I inherit .analyze_body() from MoreGenericExtractor above


def combine_feature_extractors(text: str):
    results = {}
    for fx in [
        HandTunedExtractor(),
        WordFrequencyExtractor(),
        MoreGenericExtractor(["tiny", "birds"]),
        EvenMoreGenericExtractor("/path/to/words-file.txt"),
    ]:
        print("Running", fx, "which has instance members", getattr(fx))
        print("Its class,", fx.__class_, ", has class members", getattr(fx.__class__))
        try:
            results[fx.extractor_name] = fx.analyze_body(text)
        except Exception as e:
            results[fx.extractor_name] = {"error": str(e)}
    report_lines = [
        f"Feature Extraction produced {len(results)} kinds of results.",
        "'dog' {} appear, {} times".format(
            "did" if results["MoreGenericExtractor"]["features"]["matches"]["dog"] else "did not",
            results["WordFrequencyExtractor"]["features"]["matches"].get("dog") or 0,
        ),
        "The article had {} total words, {} unique".format(
            results["MoreGenericExtractor"]["features"]["n_total_words"],
            results["WordFrequencyExtractor"]["features"]["n_unique_words"],
        )
    ]
    return "\n\n".join(report_lines), results


# from pathlib import Path


# class FeatureExtractor:
#     def __init__(self):
#         # default constructor
#         self.extractor_name = self.__class__.__name__  # something unique


# class SimpleExtractor(FeatureExtractor):
#     def analyze_body(self, text, **context):
#         # I don't even care about the context (like a dictionary)
#         return {
#             "I am very smart": False,
#             "features": {
#                 "dog": "dog" in text.lower(),
#                 "pet": "pet" in text.lower(),
#                 "animal": "animal" in text.lower(),
#             }
#         }


# class HandTunedExtractor(FeatureExtractor):
#     def analyze_body(self, text, **context):
#         # I don't even care about the context
#         return {
#             "version": "2.0",
#             "features": {
#                 "finding": "dog" in text.lower() and not "dawg" in text.lower()
#             }
#         }


# class VerySophisticatedExtractor(FeatureExtractor):
#     def __init__(self, local_state_path):
#         # I have a slow startup
#         local_state_path = Path(local_state_path)  # turn a string into a path Python can use
#         self.extractor_name = "{}/{}".format(self.__class__.__name__, local_state_path)
#         super().__init__()  # calls the ancestral .__init__ of FeatureExtractor above
#         self.data = local_state_path.read_bytes()

#     def analyze_body(self, text, publication_date=None, **context):
#         # I do use some context
#         if publication_date.year > 2022:
#             raise ValueError("This article is from the future")
#             # execution would stop here
#         return {
#             "git-commit": "cafebee",
#             **some_big_third_party_GPU_miner.extract_keywords(
#                 text.decode(),
#                 massive_other_stuff=self.data,
#                 whole_buncha_contaxt=context,
#             ),
#         }


# def combine_feature_extractors(text):
#     results = {}
#     for fx in [
#         SimpleExtractor(),
#         HandTunedExtractor(),
#         VerySophisticatedExtractor("/some/ML/data/here"),
#         VerySophisticatedExtractor("/some/different/ML/data/here"),
#         VerySophisticatedExtractor("/you/can/keep/going/with/more/data"),
#     ]:
#         try:
#             results[fx.extractor_name] = fx.analyze_body(text, publication_date=2022, timeout=100.)
#         except Exception as e:
#             results[fx.extractor_name] = {"error": str(e)}
#     # up to you to jam the results together in an intelligent way - maybe pruning the dictionary result
#     return results  # or not