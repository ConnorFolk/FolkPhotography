gcloud builds submit --tag gcr.io/sublimecoverbandits/sublime-cover-bandits --project=sublimecoverbandits


gcloud run deploy sublime-cover-bandits --image gcr.io/sublimecoverbandits/sublime-cover-bandits --platform managed --project=sublimecoverbandits --allow-unauthenticated --region us-east1