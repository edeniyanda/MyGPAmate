class convert_score_to_grade:
    def __init__(self, scores:list) -> None:
        self.scores = scores
        self.grade_list = []
    def convert(self) -> dict:
        for i in self.scores:
            if i >= 70:
                self.grade_list.append("A")
            elif i >= 60:
                self.grade_list.append("B")
            elif i >= 50:
                self.grade_list.append("C")
            elif i >= 45:
                self.grade_list.append("D")
            elif i >= 40:
                self.grade_list.append("E")
            else:
                self.grade_list.append("F")
        
        return self.grade_list
        

