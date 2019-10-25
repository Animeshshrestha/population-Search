from django.shortcuts import render

# from pusher import Pusher

# pusher = Pusher(
#     app_id='814492',
#     key='103ebaaa5395c0e58d67',
#     secret='4eb627ea6d3ec2136429',
#     cluster='ap2',
#     ssl=True)

def hello(request):
	# pusher.trigger(u'a_channel', u'an_event', {u'message': 'hello world'})

	return render(request,'population.html')
