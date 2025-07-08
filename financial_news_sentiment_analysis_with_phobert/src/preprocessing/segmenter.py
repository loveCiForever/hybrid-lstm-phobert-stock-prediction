from vncorenlp import VnCoreNLP

def segment_texts(texts, vncorenlp_path:str="vncorenlp/VnCoreNLP-1.2.jar"):
    segmenter = VnCoreNLP(vncorenlp_path)
    segmented = [' '.join([' '.join(sent) for sent in segmenter.tokenize(text)]) for text in texts]
    segmenter.close()
    return segmented