import json
import os

import state

class Lesson:
    def __init__(self, title: str, id: str, lines: list[str]):
        self.title = title
        self.id = id
        self.lines = lines

    @staticmethod
    def load(lesson_id: str):
        """
        Loads a lesson from the lesson folder with the specified lesson id.
        
        :type lesson_id: str
        :rtype: Lesson
        """
        with open(f"{state.LESSONS_FP}\\{lesson_id}.json") as lesson_file:
            lesson_data = json.load(lesson_file)

        return Lesson(**lesson_data)
    
lessons: list[Lesson] = []
def load_lessons():
    """
    Loads the lessons in bin/lessons into the global lessons variable
    """
    global lessons
    for lesson_fp in os.listdir(state.LESSONS_FP):
        lessons.append(Lesson.load(lesson_fp.split('\\')[-1].removesuffix('.json')))