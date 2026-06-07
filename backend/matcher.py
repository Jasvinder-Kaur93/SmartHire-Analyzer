from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_match_score(
    resume_text,
    job_desc
):

    if not resume_text.strip():

        return 0

    if not job_desc.strip():

        return 0

    tfidf = TfidfVectorizer(
        stop_words='english'
    )

    matrix = tfidf.fit_transform([
        resume_text,
        job_desc
    ])

    similarity = cosine_similarity(
        matrix[0:1],
        matrix[1:2]
    )

    return round(
        float(similarity[0][0]) * 100,
        2
    )