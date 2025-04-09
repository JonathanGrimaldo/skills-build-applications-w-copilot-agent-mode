from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(
            settings.DATABASES['default']['CLIENT'].get('host', 'mongodb://localhost'),
            settings.DATABASES['default']['CLIENT'].get('port', 27017)
        )
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Crear usuarios sin el campo _id, ya que Django genera automáticamente el campo id
        users = [
            User(username='thundergod', email='thundergod@mhigh.edu', password='thundergodpassword'),
            User(username='metalgeek', email='metalgeek@mhigh.edu', password='metalgeekpassword'),
            User(username='zerocool', email='zerocool@mhigh.edu', password='zerocoolpassword'),
            User(username='crashoverride', email='crashoverride@mhigh.edu', password='crashoverridepassword'),
            User(username='sleeptoken', email='sleeptoken@mhigh.edu', password='sleeptokenpassword'),
        ]
        User.objects.bulk_create(users)

        # Guardar usuarios individualmente para asegurarse de que estén en la base de datos
        for user in users:
            user.save()

        # Crear equipos sin el campo _id, ya que Django genera automáticamente el campo id
        team1 = Team(name='Blue Team')
        team2 = Team(name='Gold Team')
        team1.save()
        team2.save()
        # Asegurarse de que los usuarios estén correctamente asociados con los equipos
        team1.members.set([users[0], users[1], users[2]])
        team2.members.set([users[3], users[4]])

        # Crear actividades sin el uso de ObjectId
        activities = [
            Activity(user=users[0], activity_type='Cycling', duration=timedelta(hours=1)),
            Activity(user=users[1], activity_type='Crossfit', duration=timedelta(hours=2)),
            Activity(user=users[2], activity_type='Running', duration=timedelta(hours=1, minutes=30)),
            Activity(user=users[3], activity_type='Strength', duration=timedelta(minutes=30)),
            Activity(user=users[4], activity_type='Swimming', duration=timedelta(hours=1, minutes=15)),
        ]
        Activity.objects.bulk_create(activities)

        # Crear entradas de leaderboard sin el uso de ObjectId
        leaderboard_entries = [
            Leaderboard(user=users[0], score=100),
            Leaderboard(user=users[1], score=90),
            Leaderboard(user=users[2], score=95),
            Leaderboard(user=users[3], score=85),
            Leaderboard(user=users[4], score=80),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Crear entrenamientos sin el uso de ObjectId
        workouts = [
            Workout(name='Cycling Training', description='Training for a road cycling event'),
            Workout(name='Crossfit', description='Training for a crossfit competition'),
            Workout(name='Running Training', description='Training for a marathon'),
            Workout(name='Strength Training', description='Training for strength'),
            Workout(name='Swimming Training', description='Training for a swimming competition'),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
