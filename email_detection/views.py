from django.shortcuts import render
from django.http import JsonResponse
from .models import EmailClassification
import joblib

# Load the trained model and vectorizer
model = joblib.load('phishing_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

def classify_email(request):
    label = None
    email_text = None
    classification_instance = None

    if request.method == 'POST':
        email_text = request.POST.get('email_text', '')
        feedback = request.POST.get('feedback', '')

        if feedback and 'classification_id' in request.POST:
            # Handle feedback submission
            classification_instance = EmailClassification.objects.get(id=request.POST.get('classification_id'))
            classification_instance.is_correct = feedback == 'correct'
            classification_instance.save()
            return JsonResponse({'message': 'Thank you for your feedback!'})

        else:
            # Preprocess the text using the loaded vectorizer
            email_tfidf = vectorizer.transform([email_text])

            # Predict using the loaded model
            prediction = model.predict(email_tfidf)

            # Convert prediction to readable label
            label = 'phishing' if prediction[0] == 0 else 'legitimate'

            # Save the email and classification in the database
            classification_instance = EmailClassification.objects.create(
                email_text=email_text,
                classification=label
            )

            return JsonResponse({
                'label': label,
                'classification_id': classification_instance.id
            })

    return render(request, 'classify.html')
