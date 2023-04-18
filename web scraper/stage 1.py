""" Your program should send an HTTP request to a URL received from the user input. The user input can be a Quotable
resource http://api.quotable.io/quotes/-CzNrWMGIg8V. In this case, the program should print out the Quote extracted
from the json body response.

The user may also input an invalid URL or a non-existing quote resource, for example,
http://api.quotable.io/quotes/1, or a different Quotable page (http://api.quotable.io/authors).
Use if-else statements to check the status_code or the json body response.
Print out the Invalid quote resource! error message when the response code is different from 200
or when there is no quote in the json body response """