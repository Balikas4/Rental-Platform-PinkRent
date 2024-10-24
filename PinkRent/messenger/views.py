from django.shortcuts import render, get_object_or_404, redirect
from .models import Conversation, Message
from django.contrib.auth.decorators import login_required
from .forms import MessageForm
from listings.models import Listing


@login_required
def conversation_list(request):
    user = request.user

    # Get all conversations involving the user (both as sender and receiver)
    conversations = Conversation.objects.filter(sender=user) | Conversation.objects.filter(receiver=user)

    # Delete any conversations that are empty (no messages)
    for conversation in conversations:
        if not conversation.messages.exists():
            conversation.delete()

    # Refresh the conversations list after deletion
    conversations = Conversation.objects.filter(sender=user) | Conversation.objects.filter(receiver=user)

    return render(request, 'conversation_list.html', {
        'conversations': conversations,
    })



@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    # Ensure the user is part of the conversation
    if request.user not in [conversation.sender, conversation.receiver]:
        return render(request, 'error.html', {'message': "You are not authorized to view this conversation."})

    # Fetch messages
    chat_messages = conversation.messages.all()

    # Only mark messages as read if the current user is the receiver of those specific messages
    for message in chat_messages:
        if message.receiver == request.user and not message.read:
            message.read = True  # Mark the message as read
            message.save()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.read = False  # New messages are unread by default

            # Dynamically set the receiver based on who the sender is
            if request.user == conversation.sender:
                message.receiver = conversation.receiver  # The other participant is the receiver
            else:
                message.receiver = conversation.sender  # The sender is the other participant

            message.save()

            # Update last_message in the conversation
            conversation.last_message = message
            conversation.save()

            return redirect('messenger:conversation_detail', conversation_id=conversation.id)

    else:
        form = MessageForm()

    return render(request, 'conversation_detail.html', {
        'conversation': conversation,
        'chat_messages': chat_messages,
        'form': form,
    })


@login_required
def start_conversation(request, listing_id):
    # Get the listing based on the ID
    listing = get_object_or_404(Listing, id=listing_id)

    # The owner of the listing
    listing_owner = listing.owner

    # Prevent the listing owner from starting a conversation with themselves
    if request.user == listing_owner:
        return render(request, 'error.html', {'message': "You cannot start a conversation with yourself."})

    # Check if a conversation already exists between the two participants
    conversation = Conversation.objects.filter(
        sender=request.user, receiver=listing_owner, listing=listing
    ).first() or Conversation.objects.filter(
        sender=listing_owner, receiver=request.user, listing=listing
    ).first()

    # If no conversation exists, create a new one
    if not conversation:
        conversation = Conversation.objects.create(
            sender=request.user,
            receiver=listing_owner,
            listing=listing,  # Set the listing here
            last_message=None  # No messages yet
        )

    # Redirect to the conversation detail page
    return redirect('messenger:conversation_detail', conversation_id=conversation.id)
