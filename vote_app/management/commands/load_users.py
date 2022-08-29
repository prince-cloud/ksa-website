from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth import get_user_model
import csv
from django.conf import settings
from vote_app.sms import SmsApi, Sms
from accounts.utils import generate_password
from vote_app.models import Election
sms = Sms()

User = get_user_model()


class Command(BaseCommand):
    help = """
    Create users from csv file.
    Parameters:
        file_name: The name of the csv file
        level : The level of the student, must be one of 100, 200, 300, 400
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--filename",
            help="Specifies the CSV filename.",
        )
        parser.add_argument(
            "--election",
            help="specifies the id of the elections to which the news student should be registered to."
        )

    def handle(self, *args, **kwargs):
        filename = settings.BASE_DIR / kwargs["filename"]
        time = timezone.now()
        self.stdout.write(f"Loading Users in: {time}")
        election : Election = Election.objects.get(pk=kwargs['election'])

        with open(filename, "r") as f:
            c = csv.reader(f)

            for line in c:
                name, phone = line

                if User.objects.filter(username=phone.strip()).exists():
                    print(f"Skipping user {phone} with phone {phone} ")
                    continue
                first_name = name.split(" ")[0]
                last_name = " ".join(name.split(" ")[1:])
                if len(phone) < 10:
                    phone = "".join(["0", phone])
                u = User(
                    username=phone,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone,
                )
                
                password = generate_password(length=8)
                u.set_password(password)
                print('========= Printing Users ==========')
                print("User: ", u, "Password: ", password)
                try:
                    u.save()
                    message = f"Hello login to vote at https://ksa.com/elections/ with your phone number as username and      password: {password}"
                    election.voters.add(u)
                    #sms.send_message(
                    #    recipients=[u.phone_number],
                    #    message=message,
                    #    sender="KSA-EC",
                    #)

                except Exception as e:
                    self.stdout.write(str(e))

                    self.stdout.write(f"Error: User already exists {line}")
                self.stdout.write(f"Logging {line}")

        end_time = timezone.now()
        self.stdout.write(f"Completed Loading Users : {end_time}")
