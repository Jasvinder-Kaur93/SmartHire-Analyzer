TECH_SKILLS = {

    "Programming": [

        "python",
        "java",
        "c++",
        "javascript"

    ],

    "Web": [

        "html",
        "css",
        "react",
        "django",
        "flask"

    ],

    "Database": [

        "sql",
        "mysql",
        "mongodb"

    ],

    "Cloud": [

        "aws",
        "azure",
        "docker"

    ],

    "AI": [

        "machine learning",
        "deep learning",
        "nlp"

    ]
}


def extract_skills(text):

    found = []

    text = text.lower()

    for category, skills in TECH_SKILLS.items():

        for skill in skills:

            if skill.lower() in text:
                found.append(skill)

    return sorted(
        list(set(found))
    )