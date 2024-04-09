from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Offer, Listing
from .forms import OfferForm

@login_required
def send_offer(request, listing_id=None):
    listing = None
    if listing_id is not None:
        listing = get_object_or_404(Listing, pk=listing_id)
    
    if request.method == 'POST':
        form = OfferForm(request.user, listing, request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.sender = request.user
            offer.listing = listing
            offer.save()
            messages.success(request, 'Offer sent successfully.')
            return redirect('offers:offer_sent')
    else:
        form = OfferForm(request.user, listing)

    return render(request, 'send_offer.html', {'form': form, 'listing': listing})



@login_required
def offer_sent(request):
    sent_offers = request.user.sent_offers.all()
    return render(request, 'offer_sent.html', {'sent_offers': sent_offers})

@login_required
def accept_offer(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if offer.receiver == request.user and offer.status == 'pending':
        offer.status = 'accepted'
        offer.save()
        messages.success(request, "Offer accepted successfully")
    else:
        messages.error(request, "Unable to accept the offer")

    return redirect('offers:my_offers')

@login_required
def reject_offer(request, pk):
    # Implement the logic for rejecting an offer
    offer = get_object_or_404(Offer, pk=pk)
    if offer.receiver == request.user and offer.status == 'pending':
        offer.status = 'rejected'
        offer.save()
        messages.success(request, "Offer rejected successfully")
    else:
        messages.error(request, "Unable to reject the offer")

    return redirect('offers:my_offers')

@login_required
def my_offers(request):
    incoming_offers = Offer.objects.filter(receiver=request.user)
    sent_offers = Offer.objects.filter(sender=request.user)
    context = {
        'incoming_offers': incoming_offers,
        'sent_offers': sent_offers,
    }

    return render(request, 'my_offers.html', context)

def offer_details(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    if request.user != offer.sender and request.user != offer.receiver:
        return render(request, 'offer_details_permission_denied.html')
    context = {
        'offer': offer,
    }
    return render(request, 'offer_details.html', context)
