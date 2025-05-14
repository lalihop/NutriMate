import tkinter as tk
from tkinter import messagebox
from scipy.optimize import linprog
import numpy as np
import pandas as pd

# Load the food nutrition data
file_path = 'food.xlsx'
food_df = pd.read_excel(file_path)

# Remove rows with invalid values
food_df = food_df.replace([np.inf, -np.inf], np.nan).dropna()

user = {}
breakfast = {}
lunch = {}
dinner = {}

def get_valid_input(entry, error_msg, valid_func):
    try:
        value = valid_func(entry.get())
        return value
    except ValueError:
        messagebox.showerror("입력 오류", error_msg)
        return None

def input_user_info():
    global user
    user['height'] = get_valid_input(height_entry, "유효한 정수 값을 입력해주세요.", int)
    user['weight'] = get_valid_input(weight_entry, "유효한 정수 값을 입력해주세요.", int)
    user['age'] = get_valid_input(age_entry, "유효한 정수 값을 입력해주세요.", int)
    gender = gender_var.get()
    if gender in ['남', '여']:
        user['gender'] = gender
    else:
        messagebox.showerror("입력 오류", "유효한 값을 입력해주세요.")

    if None not in user.values():
        calculate_bmr_tdee()

def calculate_bmr(weight, height, age, gender):
    if gender == '남':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    elif gender == '여':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    return bmr

def calculate_tdee(bmr, activity_level):
    activity_multipliers = {
        '1': 1.2,
        '2': 1.375,
        '3': 1.55,
        '4': 1.725,
        '5': 1.9
    }
    return bmr * activity_multipliers[activity_level]

def calculate_macros(calories, carb_ratio, protein_ratio, fat_ratio):
    carbs = (calories * carb_ratio) / 4
    protein = (calories * protein_ratio) / 4
    fat = (calories * fat_ratio) / 9
    return carbs, protein, fat

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def calculate_bmr_tdee():
    global user
    age = user['age']
    gender = user['gender']
    weight = user['weight']
    height = user['height']

    activity_window = tk.Toplevel(root)
    activity_window.title("활동 수준")

    tk.Label(activity_window, text="활동 수준을 선택하세요:").pack()

    def set_activity_level(level):
        global tdee, target_calories, carbs, protein, fat
        bmr = calculate_bmr(weight, height, age, gender)
        tdee = calculate_tdee(bmr, level)

        diet_goal_window = tk.Toplevel(root)
        diet_goal_window.title("식단 조절 프로그램 사용 목적")

        tk.Label(diet_goal_window, text="식단 조절 프로그램 사용 목적을 선택하세요:").pack()

        def set_diet_goal(goal):
            global target_calories, carbs, protein, fat
            if goal == '1':
                target_calories = tdee - 500
                carb_ratio, protein_ratio, fat_ratio = 0.45, 0.35, 0.20
            elif goal == '2':
                target_calories = tdee + 300
                carb_ratio, protein_ratio, fat_ratio = 0.50, 0.30, 0.20
            elif goal == '3':
                target_calories = tdee
                carb_ratio, protein_ratio, fat_ratio = 0.05, 0.20, 0.75

            carbs, protein, fat = calculate_macros(target_calories, carb_ratio, protein_ratio, fat_ratio)

            messagebox.showinfo("추천 섭취량", f"칼로리 섭취량: {target_calories:.2f} kcal/day\n탄수화물 섭취량: {carbs:.2f} g/day\n단백질 섭취량: {protein:.2f} g/day\n지방 섭취량: {fat:.2f} g/day")
            diet_goal_window.destroy()
            input_meals()

        tk.Button(diet_goal_window, text="체중 감량", command=lambda: set_diet_goal('1')).pack()
        tk.Button(diet_goal_window, text="근육 증가", command=lambda: set_diet_goal('2')).pack()
        tk.Button(diet_goal_window, text="케토", command=lambda: set_diet_goal('3')).pack()

        center_window(diet_goal_window)
        activity_window.destroy()

    tk.Button(activity_window, text="거의 활동 없음", command=lambda: set_activity_level('1')).pack()
    tk.Button(activity_window, text="가벼운 활동", command=lambda: set_activity_level('2')).pack()
    tk.Button(activity_window, text="보통 활동", command=lambda: set_activity_level('3')).pack()
    tk.Button(activity_window, text="활동적", command=lambda: set_activity_level('4')).pack()
    tk.Button(activity_window, text="매우 활동적", command=lambda: set_activity_level('5')).pack()

    center_window(activity_window)

def input_meals():
    meal_window = tk.Toplevel(root)
    meal_window.title("식사 입력")

    tk.Label(meal_window, text="아침에 먹은 총 칼로리/탄수화물/단백질/지방의 값을 입력해주세요 (예: 1000/150/80/100)").pack()
    breakfast_entry = tk.Entry(meal_window)
    breakfast_entry.pack()

    tk.Label(meal_window, text="점심에 먹은 총 칼로리/탄수화물/단백질/지방의 값을 입력해주세요 (예: 1000/150/80/100)").pack()
    lunch_entry = tk.Entry(meal_window)
    lunch_entry.pack()

    def save_meals():
        breakfast_values = breakfast_entry.get().split('/')
        lunch_values = lunch_entry.get().split('/')
        if len(breakfast_values) == 4 and len(lunch_values) == 4:
            breakfast['총 열량'], breakfast['탄수화물'], breakfast['단백질'], breakfast['지방'] = map(float, breakfast_values)
            lunch['총 열량'], lunch['탄수화물'], lunch['단백질'], lunch['지방'] = map(float, lunch_values)

            remaining_calories = target_calories - breakfast['총 열량'] - lunch['총 열량']
            remaining_carbs = carbs - breakfast['탄수화물'] - lunch['탄수화물']
            remaining_protein = protein - breakfast['단백질'] - lunch['단백질']
            remaining_fat = fat - breakfast['지방'] - lunch['지방']

            recommend_dinner(remaining_calories, remaining_carbs, remaining_protein, remaining_fat)
        else:
            messagebox.showerror("입력 오류", "모든 값을 정확히 입력해주세요.")

    tk.Button(meal_window, text="저장", command=save_meals).pack()
    center_window(meal_window)

def recommend_dinner(remaining_calories, remaining_carbs, remaining_protein, remaining_fat):
    global food_df

    # Objective function: Minimize the sum of selected foods
    c = np.ones(len(food_df))

    # Constraints
    A = np.array([
        food_df['에너지(㎉)'].values,
        food_df['탄수화물(g)'].values,
        food_df['단백질(g)'].values,
        food_df['지방(g)'].values
    ])
    b = np.array([remaining_calories, remaining_carbs, remaining_protein, remaining_fat])

    bounds = [(0, None)] * len(food_df)

    res = linprog(c, A_eq=A, b_eq=b, bounds=bounds, method='highs')

    if res.success:
        selected_foods = res.x > 0
        recommended_foods = food_df[res.x > 0]

        # Select one food with '밥' in its name
        rice_food = recommended_foods[recommended_foods['식품명'].str.contains('밥', na=False)].head(1)

        # Select one food with '국' in its name
        soup_food = recommended_foods[recommended_foods['식품명'].str.contains('국', na=False)].head(1)

        # Select one more food excluding the ones already selected
        remaining_foods = recommended_foods[~recommended_foods.index.isin(rice_food.index) &
                                            ~recommended_foods.index.isin(soup_food.index)].head(1)

        final_recommendations = pd.concat([rice_food, soup_food, remaining_foods])

        recommendations = "\n".join(f"{row['식품명']}: {round(row['에너지(㎉)'], 2)} kcal, {round(row['탄수화물(g)'], 2)}g, {round(row['단백질(g)'], 2)}g, {round(row['지방(g)'], 2)}g" for index, row in final_recommendations.iterrows())
        messagebox.showinfo("저녁 추천 메뉴", f"남은 영양소를 채우기 위한 추천 메뉴:\n\n{recommendations}")
    else:
        messagebox.showerror("오류", "추천 메뉴를 찾지 못했습니다. 입력 값을 다시 확인해주세요.")

root = tk.Tk()
root.title("저녁 메뉴 추천 프로그램")

tk.Label(root, text="사용자의 키를 입력하세요.(cm):").pack()
height_entry = tk.Entry(root)
height_entry.pack()

tk.Label(root, text="사용자의 몸무게를 입력하세요.(kg):").pack()
weight_entry = tk.Entry(root)
weight_entry.pack()

tk.Label(root, text="나이를 입력하세요:").pack()
age_entry = tk.Entry(root)
age_entry.pack()

tk.Label(root, text="사용자의 성별을 선택하세요:").pack()
gender_var = tk.StringVar(value="남")
tk.Radiobutton(root, text="남", variable=gender_var, value="남").pack()
tk.Radiobutton(root, text="여", variable=gender_var, value="여").pack()

tk.Button(root, text="정보 저장", command=input_user_info).pack()

center_window(root)
root.mainloop()
