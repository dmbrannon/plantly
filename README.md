# plantly
:seedling: A plant watering schedule web application built using Django, hosted on DigitalOcean at www.plantly.tech.
> Dana M. Brannon

## About this application
I love house plants. There are [quite](https://rightasrain.uwmedicine.org/life/leisure/health-benefits-indoor-plants) [a](https://www.psychologytoday.com/us/blog/cravings/201909/11-ways-plants-enhance-your-mental-and-emotional-health) [few](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4419447/) studies on how indoor plants can be beneficial to the psychological wellbeing of occupants. But we must remember that they are living things (not just decorations!) and therefore need consistent care and attention in order to stay alive. 

I first created an iOS app during my Mobile Computing class that helped remind me when to water my plants, as well as keep a log on each plant to record things like fertilization, repotting, pest control, etc. I realized I wanted to move this to a web based application because I didn't want to pay the (somewhat exorbitant) fees to keep it on the App Store. I decided this would be a great opportunity to get experience with a framework I've been wanting to learn for quite a while now: **Django**. So this app is my journey to learn Django, and to eventually deploy the app on DigitalOcean with Docker.

## Steps I took to create this application
1. **Learn Django:** I'm definitely still in the process of learning the framework, but some resources that really helped me out are the [Django Documentation](https://docs.djangoproject.com/en/3.0/intro/tutorial01/) as well as [Corey Schafer's YouTube series](https://www.youtube.com/watch?v=UmljXZIypDc) on Django (and of course lots of Stack Overflow!)

2. **Choose a Hosting service:** I went with [DigitalOcean](https://www.digitalocean.com/) because the [GitHub Student Developer Pack](https://education.github.com/pack) gives you $50 in free credit.

3. **Set up my new DigitalOcean droplet:** A <i>droplet</i> is what DigitalOcean calls its scalable virtual machines. This step involved a lot of sysadmin stuff, which I enjoyed getting exposure to. Plus, DigitalOcean has some great resources for this type of stuff (see the [Initial Server Setup guide](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-18-04) for help on setting up SSH, creating a sudo-enabled user, setting up a basic firewall, etc)

4. **Set up my Django project with Postgres, Nginx and Gunicorn:** My DigitalOcean droplet is running on Ubuntu 18.04 (a Linux operating system), which is what I am most comfortable with (our CS department servers were also on Ubuntu). [This guide](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04) did a flawless job of getting my Django project up and running on my droplet.

5. **Use a Domain Name Registrar:** The only way to access my website at first was through an ugly IP address (ex. 123.456.789.01). To fix this, you have to go through a company called a domain name registrar, which manage the reservation of Internet domain names. There are a couple of free-for-1-year options on the [GitHub Student Developer Pack](https://education.github.com/pack), which I would highly recommend checking out. Obviously, I went with www.plantly.tech

6. **Get a Free SSL Certificate:** An SSL certificate is a type of digital certificate that provides authentication for your website and enables an encrypted connection. This means your website will start with <i>HTTPS</i> instead of <i>HTTP</i>. Basically, this just means your internet traffic will be encrypted (to keep your users' data secure!) DigitalOcean has another great guide on [securing Nginx with Let's Encrypt](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04), which allows you to get a FREE SSL certificate!

7. **Make sure my environment is production-ready:** This was probably the trickiest step (aside from making the actual application), because I have never deployed anything before. What made it even trickier is that everyone and their dog has a different methodology for deploying Django apps. I went ahead and just used environment variables to store different settings for my development and production environments. I'm not totally sure if that's the best way to do it, so if anyone has suggestions, feel free to [email me](mailto:dana.brannon@utexas.edu).

This has been a great learning experience so far, and I honestly can't wait to keep learning more. 😃
