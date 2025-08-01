import json
import os
import tkinter as tk
from tkinter import messagebox
import calendar
from datetime import date

DATA_FILE = "dane.json"


def wczytaj_dane():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def zapisz_dane(dane):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dane, f, indent=4, ensure_ascii=False)


class CalendarWidget(tk.Toplevel):
    def __init__(self, master, date_var):
        super().__init__(master)
        self.date_var = date_var
        self.title("Wybierz datę")
        self.resizable(False, False)

        today = date.today()
        self.year = today.year
        self.month = today.month

        self.header = tk.Label(self, text="", font=("Arial", 12, "bold"))
        self.header.grid(row=0, column=1, columnspan=5, pady=5)

        tk.Button(self, text="<", command=self.prev_month).grid(row=0, column=0)
        tk.Button(self, text=">", command=self.next_month).grid(row=0, column=6)

        self.day_buttons = []
        for i in range(6):
            row = []
            for j in range(7):
                btn = tk.Button(self, text="", width=3, command=lambda d=0: None)
                btn.grid(row=i+1, column=j, padx=2, pady=2)
                row.append(btn)
            self.day_buttons.append(row)

        self.draw_calendar()

    def draw_calendar(self):
        self.header.config(text=f"{calendar.month_name[self.month]} {self.year}")
        monthcal = calendar.monthcalendar(self.year, self.month)
        for i in range(6):
            for j in range(7):
                try:
                    day = monthcal[i][j]
                except IndexError:
                    day = 0
                btn = self.day_buttons[i][j]
                if day == 0:
                    btn.config(text="", state="disabled", command=lambda d=0: None)
                else:
                    btn.config(text=str(day), state="normal", command=lambda d=day: self.set_date(d))

    def set_date(self, day):
        selected = date(self.year, self.month, day)
        self.date_var.set(selected.isoformat())
        self.destroy()

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.draw_calendar()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.draw_calendar()


class OvertimeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ewidencja nadgodzin")
        self.geometry("350x300")
        self.dane = wczytaj_dane()

        tk.Label(self, text="Pracownik").grid(row=0, column=0, pady=5)
        tk.Label(self, text="Data").grid(row=1, column=0, pady=5)
        tk.Label(self, text="Godziny").grid(row=2, column=0, pady=5)

        self.pracownik_var = tk.Entry(self)
        self.pracownik_var.grid(row=0, column=1)

        self.data_var = tk.StringVar()
        self.data_entry = tk.Entry(self, textvariable=self.data_var)
        self.data_entry.grid(row=1, column=1)
        tk.Button(self, text="Kalendarz", command=self.open_calendar).grid(row=1, column=2, padx=5)

        self.godziny_var = tk.Entry(self)
        self.godziny_var.grid(row=2, column=1)

        tk.Button(self, text="Dodaj nadgodziny", command=self.dodaj_nadgodziny).grid(row=3, column=0, pady=10)
        tk.Button(self, text="Odbierz nadgodziny", command=self.odbierz_nadgodziny).grid(row=3, column=1, pady=10)
        tk.Button(self, text="Pokaż saldo", command=self.pokaz_saldo).grid(row=4, column=0, columnspan=2)

    def open_calendar(self):
        CalendarWidget(self, self.data_var)

    def dodaj_nadgodziny(self):
        nazwisko = self.pracownik_var.get().strip()
        data_val = self.data_var.get().strip()
        try:
            godziny = float(self.godziny_var.get())
        except ValueError:
            messagebox.showerror("Błąd", "Wprowadź poprawną liczbę godzin.")
            return

        if nazwisko and data_val:
            self.dane.setdefault(nazwisko, {"wypracowane": [], "odebrane": []})
            self.dane[nazwisko]["wypracowane"].append({"data": data_val, "godziny": godziny})
            zapisz_dane(self.dane)
            messagebox.showinfo("OK", "Nadgodziny dodane.")
        else:
            messagebox.showerror("Błąd", "Uzupełnij wszystkie pola.")

    def odbierz_nadgodziny(self):
        nazwisko = self.pracownik_var.get().strip()
        data_val = self.data_var.get().strip()
        try:
            godziny = float(self.godziny_var.get())
        except ValueError:
            messagebox.showerror("Błąd", "Wprowadź poprawną liczbę godzin.")
            return

        if nazwisko and data_val:
            saldo = self.oblicz_saldo(nazwisko)
            if godziny > saldo:
                messagebox.showerror("Błąd", "Nie można odebrać więcej godzin niż dostępne.")
                return
            self.dane.setdefault(nazwisko, {"wypracowane": [], "odebrane": []})
            self.dane[nazwisko]["odebrane"].append({"data": data_val, "godziny": godziny})
            zapisz_dane(self.dane)
            messagebox.showinfo("OK", "Nadgodziny odebrane.")
        else:
            messagebox.showerror("Błąd", "Uzupełnij wszystkie pola.")

    def pokaz_saldo(self):
        nazwisko = self.pracownik_var.get().strip()
        if nazwisko:
            saldo = self.oblicz_saldo(nazwisko)
            messagebox.showinfo("Saldo", f"Aktualne saldo {nazwisko}: {saldo} h")
        else:
            messagebox.showerror("Błąd", "Podaj nazwisko.")

    def oblicz_saldo(self, nazwisko):
        dane_pracownika = self.dane.get(nazwisko, {"wypracowane": [], "odebrane": []})
        wypracowane = sum(item["godziny"] for item in dane_pracownika["wypracowane"])
        odebrane = sum(item["godziny"] for item in dane_pracownika["odebrane"])
        return wypracowane - odebrane


if __name__ == "__main__":
    app = OvertimeApp()
    app.mainloop()
