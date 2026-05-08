MAX_GRADE = 100
MIN_GRADE = 0
FAILING_GRADE = 55

def get_nr_of_students() -> int:
    while True:
        try:
            nr_of_students=int(input("Enter the number of students: "))
            if nr_of_students > 0:
                return nr_of_students
            else:
                print("Invalid input. Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

def get_grade(subject: str) -> float:
    while True:
        try:
            grade=float(input(f"Enter the student's grade for {subject}: "))
            if MIN_GRADE <= grade <= MAX_GRADE:
                return float(grade)
            else:
                print("Invalid input. Please enter a number between 0 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 10.")


def calculate_failing_grades(students: list) -> dict:
    failing_students = {}
    total_failing_grades = 0
    for student in students:
        nr_of_failing_grades = 0
        if student["English"] <= FAILING_GRADE:
            nr_of_failing_grades += 1
        if student["Math"] <= FAILING_GRADE:
            nr_of_failing_grades += 1
        failing_students[student["name"]] = nr_of_failing_grades
        total_failing_grades += nr_of_failing_grades
    failing_students["Total Failing Grades"] = total_failing_grades
    return failing_students


def print_student_info(students: list):
    for student in students:
        print(f"Name: {student['name']}")
        print(f"English Grade: {student['English']}")
        print(f"Math Grade: {student['Math']}")
        print("==========================================")

def calculate_average_grades(students: list) -> dict:
    """
    Calculate the average grades for each topic and overall average."""
    # Calculate average for each topic
    topics=["English", "Math"]
    average_grades_students={}
    for topic in topics:
        for student in students:
            if topic in student:
                if topic not in average_grades_students:
                    average_grades_students[topic] = 0
                average_grades_students[topic] += student[topic]
        average_grades_students[topic] /= len(students)
    
    # Calculate overall average
    total_average = sum(average_grades_students.values()) / len(average_grades_students)
    average_grades_students["Overall"] = total_average

    #this trick is needed as the requirements for this exercise
    #indicate that a tuple should be returned. Wouldn't it make
    #more sense to return a dictionary instead?
    # print("dict: ", average_grades_students)
    avg_grades_students_tuple = tuple()
    for topic, average in average_grades_students.items():
        avg_grades_students_tuple += (f"{topic}: {average:.2f}",)
    # print("tuple: ", avg_grades_students_tuple)
    return avg_grades_students_tuple

def get_student_info():
    student_info={}
    while True:
        try:
            student_name=""
            name=input("Enter the student's name: ")
            names=name.split()
            for name in names:
                name = name.strip()
                if not name.isalpha():
                    print("Invalid input. Please enter a valid name.")
                    raise ValueError("Invalid name")
                else:
                    student_name += name + " "
            student_name = student_name.strip()
        except ValueError:
            pass
        else:
            student_info["name"] = student_name
            break
    student_info["English"] = get_grade("English")
    student_info["Math"] = get_grade("Math")
    return student_info


def main():
    student_list = []
    for student_nr in range(get_nr_of_students()):
        print("==========================================")
        student_list.append(get_student_info())

    print_student_info(student_list)
    average_grades = calculate_average_grades(student_list)

    print("Average Grades:")
    for item in average_grades:
        print(item)

    print("==========================================")
    print("=========== Failing Grades: ==============")
    print("==========================================")
    current_key = 0
    failing_grades = calculate_failing_grades(student_list)
    for keys, values in failing_grades.items():
        if len(keys) > current_key-1:
            print(f"{keys}: {values} failing grade(s)")
            current_key += 1
        else:
            print(f"Total number of failing grades accross all students: {values} failing grade(s)")

if __name__ == "__main__":
    main()