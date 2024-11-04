from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserBalance, Wallet, PaymentConfirmation


@login_required
def deposit_funds(request):
    if request.method == "POST":
        amount = float(request.POST.get("amount"))
        if amount < 20.00:
            return render(request, 'payment/deposit.html', {'error': "Minimum deposit is $20."})

        # Create a new PaymentConfirmation with a 'Pending' status for manual verification
        payment_confirmation = PaymentConfirmation.objects.create(
            user=request.user,
            currency="USD",  # or dynamically based on selected currency
            transaction_id="dummy_transaction_id",  # This should come from actual payment data
            amount=amount,
            status='Pending'  # Set to Pending for manual verification
        )

        # Render a confirmation page with instructions
        return render(request, 'payment/confirm_deposit.html', {
            'transaction_id': payment_confirmation.transaction_id,
            'amount': amount
        })

    wallets = Wallet.objects.all()
    return render(request, 'payment/deposit.html', {'wallets': wallets})


@login_required
def user_balance(request):
    balance, created = UserBalance.objects.get_or_create(user=request.user)
    return render(request, 'payment/balance.html', {'balance': balance})


@login_required
def manage_wallet(request):
    if request.method == "POST":
        # Here, implement logic for the manager to update the wallet address
        currency = request.POST.get("currency")
        new_address = request.POST.get("new_address")
        wallet, created = Wallet.objects.get_or_create(currency=currency)
        wallet.address = new_address
        wallet.save()
        return redirect('manage_wallet')  # Redirect after saving

    wallets = Wallet.objects.all()
    return render(request, 'payment/manage_wallet.html', {'wallets': wallets})


@login_required
def verify_payment(request):
    if not request.user.is_staff:  # Ensure the user is a manager or staff
        return redirect('base:index')

    payments = PaymentConfirmation.objects.filter(status='Pending')
    return render(request, 'payment/verify_payments.html', {'payments': payments})


@login_required
def confirm_payment(request, transaction_id):
    if not request.user.is_staff:  # Ensure the user is a manager or staff
        return redirect('index')

    payment = get_object_or_404(PaymentConfirmation, transaction_id=transaction_id)

    if request.method == 'POST':
        # Update user balance on confirmation
        balance, created = UserBalance.objects.get_or_create(user=payment.user)
        balance.balance += payment.amount
        balance.save()

        # Mark payment as verified
        payment.status = 'Verified'
        payment.save()

        return redirect('verify_payments')  # Redirect back to the verification page

    return render(request, 'payment/confirm_payment.html', {'payment': payment})