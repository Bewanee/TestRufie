import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class BeckAnxietyTest:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Шкала тревожности Бека (BAI)")
        self.window.geometry("800x600")
        self.window.configure(bg='#f0f0f0')

        self.users_file = "users.json"
        self.history_file = "test_history.txt"  # Файл для текстовой истории
        self.current_user = None

        self.symptoms = [
            "Ощущение онемения или покалывания в теле",
            "Ощущение жары",
            "Неспособность расслабиться",
            "Страх, что произойдет самое плохое",
            "Учащенное сердцебиение",
            "Неустойчивость",
            "Нервозность",
            "Ощущение удушья",
            "Страх потерять контроль",
            "Затрудненность дыхания",
            "Испуг",
            "Нарушение пищеварения или дискомфорт в животе"
        ]

        self.current_question = 0
        self.answers = [0] * len(self.symptoms)
        self.total_score = 0

        self.create_login_screen()

    def load_users(self):
        """Загрузка данных пользователей из файла"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_users(self, users):
        """Сохранение данных пользователей в файл"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

    def save_to_text_history(self, event):
        """Сохранение события в текстовый файл истории"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.history_file, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} - {event}\n")

    def save_test_result(self):
        """Сохранение результата теста пользователя"""
        if not self.current_user:
            return

        users = self.load_users()
        if self.current_user in users:
            test_result = {
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'score': self.total_score,
                'answers': self.answers
            }

            if 'test_history' not in users[self.current_user]:
                users[self.current_user]['test_history'] = []

            users[self.current_user]['test_history'].append(test_result)
            self.save_users(users)

            # Сохраняем в текстовый файл
            result_text = f"Тест завершен: {self.current_user} - {self.total_score} баллов"
            if self.total_score <= 12:
                level = "НИЗКИЙ уровень"
            elif self.total_score <= 20:
                level = "СРЕДНИЙ уровень"
            else:
                level = "ВЫСОКИЙ уровень"

            detailed_result = f"""
{'='*60}
ТЕСТ ТРЕВОЖНОСТИ БЕКА - РЕЗУЛЬТАТ
{'='*60}
Пользователь: {self.current_user}
Дата: {test_result['date']}
Суммарный балл: {self.total_score}
Уровень тревожности: {level}

Ответы:
"""
            for i, (symptom, answer) in enumerate(zip(self.symptoms, self.answers), 1):
                detailed_result += f"{i}. {symptom}: {answer} баллов\n"

            detailed_result += f"\nРекомендации: {self.get_recommendations_text()}\n"
            detailed_result += "="*60 + "\n\n"

            with open(self.history_file, "a", encoding="utf-8") as f:
                f.write(detailed_result)

            # Сохраняем краткое событие
            self.save_to_text_history(f"Тест завершен - {self.current_user}: {self.total_score} баллов ({level})")

    def get_recommendations_text(self):
        """Получить текстовые рекомендации"""
        if self.total_score <= 12:
            return "Продолжайте практиковать здоровые coping-стратегии, поддерживайте физическую активность, соблюдайте режим сна"
        elif self.total_score <= 20:
            return "Рекомендуется освоить техники релаксации, обратить внимание на режим дня, рассмотреть консультацию психолога"
        else:
            return "Рекомендуется обратиться к психологу или психотерапевту, не откладывайте обращение за поддержкой"

    def create_login_screen(self):
        """Создание экрана регистрации/входа"""
        for widget in self.window.winfo_children():
            widget.destroy()

        # Сохраняем событие запуска приложения
        self.save_to_text_history("Запуск приложения")

        title_label = tk.Label(self.window, text="ШКАЛА ТРЕВОЖНОСТИ БЕКА (BAI)",
                              font=('Arial', 16, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=20)

        login_frame = tk.Frame(self.window, bg='#f0f0f0')
        login_frame.pack(pady=30)

        # Поле для имени
        name_label = tk.Label(login_frame, text="Введите ваше имя:",
                             font=('Arial', 12), bg='#f0f0f0')
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

        self.name_entry = tk.Entry(login_frame, font=('Arial', 12), width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.name_entry.focus()

        # Поле для возраста
        age_label = tk.Label(login_frame, text="Ваш возраст:",
                            font=('Arial', 12), bg='#f0f0f0')
        age_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

        self.age_entry = tk.Entry(login_frame, font=('Arial', 12), width=30)
        self.age_entry.grid(row=1, column=1, padx=10, pady=10)

        # Поле для пола
        gender_label = tk.Label(login_frame, text="Ваш пол:",
                               font=('Arial', 12), bg='#f0f0f0')
        gender_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')

        self.gender_var = tk.StringVar(value="не указан")
        gender_frame = tk.Frame(login_frame, bg='#f0f0f0')
        gender_frame.grid(row=2, column=1, padx=10, pady=10, sticky='w')

        tk.Radiobutton(gender_frame, text="Мужской", variable=self.gender_var,
                      value="мужской", font=('Arial', 10), bg='#f0f0f0').pack(side=tk.LEFT)
        tk.Radiobutton(gender_frame, text="Женский", variable=self.gender_var,
                      value="женский", font=('Arial', 10), bg='#f0f0f0').pack(side=tk.LEFT)

        # Кнопки
        button_frame = tk.Frame(self.window, bg='#f0f0f0')
        button_frame.pack(pady=20)

        login_button = tk.Button(button_frame, text="Начать тестирование",
                               command=self.login, font=('Arial', 12),
                               bg='#4CAF50', fg='white', padx=20, pady=10)
        login_button.pack(side=tk.LEFT, padx=10)

        # Показать историю пользователей
        history_button = tk.Button(button_frame, text="Показать историю",
                                 command=self.show_user_history,
                                 font=('Arial', 10), padx=15)
        history_button.pack(side=tk.LEFT, padx=10)

        # Кнопка для просмотра текстовой истории
        text_history_button = tk.Button(button_frame, text="Текстовая история",
                                      command=self.show_text_history,
                                      font=('Arial', 10), padx=15)
        text_history_button.pack(side=tk.LEFT, padx=10)

    def login(self):
        """Обработка входа/регистрации пользователя"""
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        gender = self.gender_var.get()

        if not name:
            messagebox.showerror("Ошибка", "Пожалуйста, введите ваше имя")
            return

        # Загрузка существующих пользователей
        users = self.load_users()

        # Регистрация нового пользователя или обновление данных
        if name not in users:
            users[name] = {
                'registration_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'age': age,
                'gender': gender,
                'test_count': 0
            }
            messagebox.showinfo("Добро пожаловать!", f"Добро пожаловать, {name}!")
            self.save_to_text_history(f"Зарегистрирован новый пользователь: {name} (возраст: {age}, пол: {gender})")
        else:
            # Обновление данных существующего пользователя
            users[name].update({
                'age': age,
                'gender': gender
            })
            test_count = users[name].get('test_count', 0)
            messagebox.showinfo("С возвращением!",
                              f"С возвращением, {name}!\nРанее вы прошли тест {test_count} раз(а)")
            self.save_to_text_history(f"Вход пользователя: {name}")

        # Сохранение данных пользователя
        self.save_users(users)
        self.current_user = name

        # Переход к инструкции
        self.create_welcome_screen()

    def show_text_history(self):
        """Показать текстовую историю"""
        if not os.path.exists(self.history_file):
            messagebox.showinfo("История", "Файл истории пока не создан")
            return

        history_window = tk.Toplevel(self.window)
        history_window.title("Текстовая история тестов")
        history_window.geometry("600x500")
        history_window.configure(bg='#f0f0f0')

        title_label = tk.Label(history_window, text="ТЕКСТОВАЯ ИСТОРИЯ ТЕСТОВ",
                              font=('Arial', 14, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=10)

        # Создание текстового поля для отображения истории
        text_frame = tk.Frame(history_window)
        text_frame.pack(fill='both', expand=True, padx=20, pady=10)

        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Courier New', 9))
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        # Чтение файла истории
        with open(self.history_file, 'r', encoding='utf-8') as f:
            history_content = f.read()

        text_widget.insert(tk.END, history_content)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Кнопки
        button_frame = tk.Frame(history_window, bg='#f0f0f0')
        button_frame.pack(pady=10)

        clear_button = tk.Button(button_frame, text="Очистить историю",
                               command=self.clear_text_history,
                               font=('Arial', 10), padx=15)
        clear_button.pack(side=tk.LEFT, padx=5)

        close_button = tk.Button(button_frame, text="Закрыть",
                               command=history_window.destroy,
                               font=('Arial', 10), padx=15)
        close_button.pack(side=tk.LEFT, padx=5)

    def clear_text_history(self):
        """Очистить файл истории"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            open(self.history_file, 'w').close()
            messagebox.showinfo("Успех", "История очищена")
            # Закрываем окно истории
            for widget in self.window.winfo_children():
                if isinstance(widget, tk.Toplevel):
                    widget.destroy()

    def show_user_history(self):
        """Показать историю пользователей"""
        users = self.load_users()

        if not users:
            messagebox.showinfo("История", "Пока нет сохраненных пользователей")
            return

        history_window = tk.Toplevel(self.window)
        history_window.title("История пользователей")
        history_window.geometry("500x400")
        history_window.configure(bg='#f0f0f0')

        title_label = tk.Label(history_window, text="Зарегистрированные пользователи",
                              font=('Arial', 14, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=10)

        # Создание текстового поля для отображения истории
        text_frame = tk.Frame(history_window)
        text_frame.pack(fill='both', expand=True, padx=20, pady=10)

        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Arial', 10))
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        for user, data in users.items():
            text_widget.insert(tk.END, f"👤 {user}\n")
            text_widget.insert(tk.END, f"   Возраст: {data.get('age', 'не указан')}\n")
            text_widget.insert(tk.END, f"   Пол: {data.get('gender', 'не указан')}\n")
            text_widget.insert(tk.END, f"   Тестов пройдено: {data.get('test_count', 0)}\n")

            if 'test_history' in data:
                text_widget.insert(tk.END, f"   История тестов:\n")
                for test in data['test_history'][-3:]:  # Последние 3 теста
                    text_widget.insert(tk.END, f"     - {test['date']}: {test['score']} баллов\n")

            text_widget.insert(tk.END, "-" * 40 + "\n")

        text_widget.config(state=tk.DISABLED)
        text_widget.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        close_button = tk.Button(history_window, text="Закрыть",
                               command=history_window.destroy,
                               font=('Arial', 10), padx=15)
        close_button.pack(pady=10)

    # Остальные методы остаются без изменений...
    # create_welcome_screen, start_test, show_question, save_answer,
    # previous_question, next_question, show_results, run

    def create_welcome_screen(self):
        """Создание начального экрана с инструкцией"""
        for widget in self.window.winfo_children():
            widget.destroy()

        # Сохраняем событие перехода к тесту
        self.save_to_text_history(f"Пользователь {self.current_user} начал ознакомление с тестом")

        # Приветствие пользователя
        welcome_label = tk.Label(self.window,
                               text=f"Добро пожаловать, {self.current_user}!",
                               font=('Arial', 14, 'bold'), bg='#f0f0f0')
        welcome_label.pack(pady=10)

        title_label = tk.Label(self.window, text="ШКАЛА ТРЕВОЖНОСТИ БЕКА (BAI)",
                              font=('Arial', 16, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=10)

        instruction_frame = tk.Frame(self.window, bg='#f0f0f0')
        instruction_frame.pack(pady=10, padx=20, fill='both')

        instruction_text = """
Оцените, насколько Вас беспокоил каждый из симптомов
за ПОСЛЕДНЮЮ НЕДЕЛЮ, включая сегодняшний день.

Выберите вариант ответа от 0 до 3:

0 - НЕТ (совсем не беспокоил)
1 - ЛЕГКО (беспокоил немного, но не слишком сильно)
2 - УМЕРЕННО (беспокоил сильно, но я мог это переносить)
3 - СИЛЬНО (беспокоил очень сильно, с трудом мог переносить)
        """

        instruction_label = tk.Label(instruction_frame, text=instruction_text,
                                   justify=tk.LEFT, font=('Arial', 11), bg='#f0f0f0')
        instruction_label.pack(pady=10)

        # Показать все вопросы
        questions_frame = tk.Frame(self.window, bg='#f0f0f0')
        questions_frame.pack(pady=10, padx=20, fill='both')

        questions_label = tk.Label(questions_frame, text="ВОПРОСЫ ТЕСТА:",
                                 font=('Arial', 12, 'bold'), bg='#f0f0f0')
        questions_label.pack()

        questions_text = ""
        for i, symptom in enumerate(self.symptoms, 1):
            questions_text += f"{i}. {symptom}\n"

        questions_text_widget = tk.Text(questions_frame, height=12, width=80, font=('Arial', 9))
        questions_text_widget.insert(tk.END, questions_text)
        questions_text_widget.config(state=tk.DISABLED)
        questions_text_widget.pack(pady=10)

        start_button = tk.Button(self.window, text="Начать тестирование",
                               command=self.start_test, font=('Arial', 12),
                               bg='#4CAF50', fg='white', padx=20, pady=10)
        start_button.pack(pady=20)

        back_button = tk.Button(self.window, text="← Сменить пользователя",
                              command=self.create_login_screen,
                              font=('Arial', 10), padx=15)
        back_button.pack(pady=10)

    def start_test(self):
        """Начало тестирования"""
        self.current_question = 0
        self.answers = [0] * len(self.symptoms)
        self.save_to_text_history(f"Пользователь {self.current_user} начал тестирование")
        self.show_question()

    def show_question(self):
        """Показать текущий вопрос"""
        for widget in self.window.winfo_children():
            widget.destroy()

        if self.current_question >= len(self.symptoms):
            self.show_results()
            return

        # Информация о пользователе
        user_frame = tk.Frame(self.window, bg='#f0f0f0')
        user_frame.pack(fill='x', padx=20, pady=5)

        user_label = tk.Label(user_frame, text=f"Пользователь: {self.current_user}",
                             font=('Arial', 10), bg='#f0f0f0')
        user_label.pack(side=tk.LEFT)

        # Прогресс бар
        progress_frame = tk.Frame(self.window, bg='#f0f0f0')
        progress_frame.pack(fill='x', padx=20, pady=10)

        progress_label = tk.Label(progress_frame,
                                text=f"Вопрос {self.current_question + 1} из {len(self.symptoms)}",
                                font=('Arial', 10), bg='#f0f0f0')
        progress_label.pack()

        progress = ttk.Progressbar(progress_frame, orient='horizontal',
                                 length=400, mode='determinate',
                                 maximum=len(self.symptoms), value=self.current_question + 1)
        progress.pack(pady=5)

        # Вопрос
        question_frame = tk.Frame(self.window, bg='#f0f0f0')
        question_frame.pack(pady=20, padx=20, fill='both')

        question_label = tk.Label(question_frame,
                                text=self.symptoms[self.current_question],
                                font=('Arial', 12, 'bold'), bg='#f0f0f0',
                                wraplength=600, justify=tk.LEFT)
        question_label.pack(pady=10)

        # Варианты ответов
        answers_frame = tk.Frame(self.window, bg='#f0f0f0')
        answers_frame.pack(pady=20)

        answer_var = tk.IntVar(value=self.answers[self.current_question])

        answers = [
            ("0 - НЕТ (совсем не беспокоил)", 0),
            ("1 - ЛЕГКО (беспокоил немного, но не слишком сильно)", 1),
            ("2 - УМЕРЕННО (беспокоил сильно, но я мог это переносить)", 2),
            ("3 - СИЛЬНО (беспокоил очень сильно, с трудом мог переносить)", 3)
        ]

        for text, value in answers:
            rb = tk.Radiobutton(answers_frame, text=text, variable=answer_var,
                              value=value, font=('Arial', 10), bg='#f0f0f0',
                              command=lambda: self.save_answer(answer_var.get()))
            rb.pack(anchor='w', pady=5)

        # Кнопки навигации
        nav_frame = tk.Frame(self.window, bg='#f0f0f0')
        nav_frame.pack(pady=20)

        if self.current_question > 0:
            prev_button = tk.Button(nav_frame, text="← Назад",
                                  command=self.previous_question,
                                  font=('Arial', 10), padx=15)
            prev_button.pack(side=tk.LEFT, padx=10)

        next_button = tk.Button(nav_frame, text="Далее →",
                              command=self.next_question,
                              font=('Arial', 10), padx=15, bg='#2196F3', fg='white')
        next_button.pack(side=tk.LEFT, padx=10)

        back_button = tk.Button(nav_frame, text="В главное меню",
                              command=self.create_welcome_screen,
                              font=('Arial', 10), padx=15)
        back_button.pack(side=tk.LEFT, padx=10)

    def save_answer(self, answer):
        """Сохранить ответ на текущий вопрос"""
        self.answers[self.current_question] = answer
        # Можно добавить сохранение каждого ответа в историю, но это может быть слишком подробно
        # self.save_to_text_history(f"Ответ на вопрос {self.current_question + 1}: {answer}")

    def previous_question(self):
        """Перейти к предыдущему вопросу"""
        if self.current_question > 0:
            self.current_question -= 1
            self.show_question()

    def next_question(self):
        """Перейти к следующему вопросу"""
        if self.answers[self.current_question] == 0 and self.current_question == 0:
            # Проверяем, что на первый вопрос дан ответ
            messagebox.showwarning("Внимание", "Пожалуйста, выберите ответ на текущий вопрос")
            return

        self.current_question += 1
        self.show_question()

    def show_results(self):
        """Показать результаты теста"""
        self.total_score = sum(self.answers)

        # Сохранение результата
        self.save_test_result()

        # Обновление счетчика тестов
        users = self.load_users()
        if self.current_user in users:
            users[self.current_user]['test_count'] = users[self.current_user].get('test_count', 0) + 1
            self.save_users(users)

        for widget in self.window.winfo_children():
            widget.destroy()

        # Результаты
        result_frame = tk.Frame(self.window, bg='#f0f0f0')
        result_frame.pack(pady=20, padx=20, fill='both')

        # Информация о пользователе
        user_info_label = tk.Label(result_frame,
                                 text=f"Пользователь: {self.current_user}",
                                 font=('Arial', 11), bg='#f0f0f0')
        user_info_label.pack(pady=5)

        title_label = tk.Label(result_frame, text="РЕЗУЛЬТАТ ТЕСТИРОВАНИЯ",
                              font=('Arial', 16, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=10)

        score_label = tk.Label(result_frame, text=f"Суммарный балл: {self.total_score}",
                              font=('Arial', 14), bg='#f0f0f0')
        score_label.pack(pady=5)

        # Интерпретация
        if self.total_score <= 12:
            interpretation = "НИЗКИЙ уровень тревожности"
            description = "Норма или минимальный уровень тревоги"
            color = '#4CAF50'
        elif self.total_score <= 20:
            interpretation = "СРЕДНИЙ уровень тревожности"
            description = "Умеренная тревога"
            color = '#FF9800'
        else:
            interpretation = "ВЫСОКИЙ уровень тревожности"
            description = "Выраженная тревога, рекомендуется консультация специалиста"
            color = '#F44336'

        interpretation_label = tk.Label(result_frame, text=f"Уровень тревожности: {interpretation}",
                                      font=('Arial', 12, 'bold'), fg=color, bg='#f0f0f0')
        interpretation_label.pack(pady=5)

        description_label = tk.Label(result_frame, text=f"Интерпретация: {description}",
                                   font=('Arial', 11), bg='#f0f0f0')
        description_label.pack(pady=5)

        # Шкала интерпретации
        scale_frame = tk.Frame(self.window, bg='#f0f0f0')
        scale_frame.pack(pady=10, padx=20)

        scale_label = tk.Label(scale_frame, text="Шкала интерпретации:",
                              font=('Arial', 11, 'bold'), bg='#f0f0f0')
        scale_label.pack()

        scale_text = "0-12 баллов - Низкий уровень тревожности\n13-20 баллов - Средний уровень тревожности\n21 и более баллов - Высокий уровень тревожности"
        scale_text_label = tk.Label(scale_frame, text=scale_text,
                                   font=('Arial', 10), justify=tk.LEFT, bg='#f0f0f0')
        scale_text_label.pack(pady=5)

        # Рекомендации
        recommendations_frame = tk.Frame(self.window, bg='#f0f0f0')
        recommendations_frame.pack(pady=10, padx=20)

        rec_label = tk.Label(recommendations_frame, text="РЕКОМЕНДАЦИИ:",
                            font=('Arial', 11, 'bold'), bg='#f0f0f0')
        rec_label.pack()

        if self.total_score <= 12:
            recommendations = [
                "✅ Продолжайте практиковать здоровые coping-стратегии",
                "✅ Поддерживайте регулярную физическую активность",
                "✅ Соблюдайте режим сна и отдыха"
            ]
        elif self.total_score <= 20:
            recommendations = [
                "Рекомендуется освоить техники релаксации",
                "Обратите внимание на режим дня и снижение стресса",
                "Рассмотрите возможность консультации психолога"
            ]
        else:
            recommendations = [
                "Рекомендуется обратиться к психологу или психотерапевту",
                "Регулярная профессиональная помощь может быть очень эффективной",
                "Не откладывайте обращение за поддержкой"
            ]

        for rec in recommendations:
            rec_label = tk.Label(recommendations_frame, text=rec,
                               font=('Arial', 10), justify=tk.LEFT, bg='#f0f0f0')
            rec_label.pack(anchor='w')

        # Кнопки действий
        button_frame = tk.Frame(self.window, bg='#f0f0f0')
        button_frame.pack(pady=20)

        restart_button = tk.Button(button_frame, text="Пройти тест заново",
                                 command=self.start_test,
                                 font=('Arial', 10), bg='#2196F3', fg='white', padx=15)
        restart_button.pack(side=tk.LEFT, padx=10)

        main_menu_button = tk.Button(button_frame, text="Главное меню",
                                   command=self.create_welcome_screen,
                                   font=('Arial', 10), padx=15)
        main_menu_button.pack(side=tk.LEFT, padx=10)

        exit_button = tk.Button(button_frame, text="Выход",
                              command=self.window.quit,
                              font=('Arial', 10), padx=15)
        exit_button.pack(side=tk.LEFT, padx=10)

    def run(self):
        """Запуск приложения"""
        self.window.mainloop()

if __name__ == "__main__":
    app = BeckAnxietyTest()
    app.run()