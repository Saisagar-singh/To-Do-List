from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import *
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

today = datetime.today()
while True:
    choice = input("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task"
                   "\n0) Exit\n")
    if choice == "1":
        print("Today {} {}".format(today.day, today.strftime('%b')))
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        if not rows:
            print("Nothing to do!")
        else:
            for i in rows:
                print(i)

    elif choice == "2":
        for i in range(7):
            week_day = today + timedelta(days=i)
            print("\n", week_day.strftime("%A %d %b"), ":")
            rows = session.query(Table).filter(Table.deadline == week_day.date()).all()
            if not rows:
                print("Nothing to do!")
            else:
                for j in rows:
                    print(j)

    elif choice == "3":
        count = 1
        print("\nAll tasks:")
        rows = session.query(Table).order_by(Table.deadline).all()
        if not rows:
            print("Nothing to do!")
        else:
            for i in rows:
                print("{0}. {1}. {2} {3}\n".format(count, i.task, i.deadline.day,
                                                   i.deadline.strftime('%b')))
                count += 1
        print()

    elif choice == "4":
        count = 1
        print("\nMissed tasks:")
        rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
        if not rows:
            print("Nothing is missed!")
        else:
            for j in rows:
                print("{0}. {1}. {2} {3}".format(count, j.task, j.deadline.day, j.deadline.strftime('%b')))
                count += 1
        print()

    elif choice == "5":
        print("\nEnter task")
        task_input = input()

        print("Enter deadline")
        deadline_time = input()

        new_row = Table(task=task_input, deadline=datetime.strptime(deadline_time, "%Y-%m-%d"))

        session.add(new_row)
        session.commit()

        print("The task has been added!")
        print()

    elif choice == "6":
        print("Choose the number of the task you want to delete:")
        count = 1
        rows = session.query(Table).order_by(Table.deadline).all()
        for i in rows:
            print("{0}. {1}. {2} {3}".format(count, i.task, i.deadline.day, i.deadline.strftime('%b')))
            count += 1
        ch = int(input())
        specific_row = rows[ch-1]
        session.delete(specific_row)
        session.commit()
        print("The task has been deleted!")
        print()

    elif choice == "0":
        print("\nBye!")
        exit()
