from datetime import datetime
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Order, Product
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['POST',])
def testPayment(request):
    testPaymentIntent = stripe.PaymentIntent.create(
        amount=1000,
        currency='usd',
        payment_method_types=['card'],
        receipt_email='test@example.com' 
    )

    return Response(status=status.HTTP_200_OK, data=testPaymentIntent)

@api_view(['POST',])
def saveStripeInfo(request):
    data = request.data
    order_id = data['orderId']
    payment_method_id = data['paymentMethodId']
    extra_msg = ''

    order = Order.objects.get(_id=order_id)
    email = order.user.email

    # check if customer exists
    customer_data = stripe.Customer.list(email=email).data

    if len(customer_data) == 0:
        customer = stripe.Customer.create(
            email=email,
            payment_method=payment_method_id
        )
    else:
        customer = customer_data[0]
        extra_msg = 'Customer already exists'

    try:
        paymentIntent = stripe.PaymentIntent.create(
            customer=customer,
            payment_method=payment_method_id,
            currency='usd',
            amount=int(order.totalPrice * 100),
            confirm=True
        )
        
        order.isPaid = True
        order.paidAt = datetime.now()
        order.save()

        orderItems = order.order_items.all()
        # print(orderItems);

        for item in orderItems:
            print(item.product)

            product = Product.objects.get(_id=item.product._id)

            product.countInStock -= item.qty
            product.save()

        return Response(status=status.HTTP_200_OK, data={
            'message': 'Success',
            'data': {
                'payment_intent': paymentIntent,
                'extra_msg': extra_msg
            }
        })
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={'detail': 'Something went wrong'})