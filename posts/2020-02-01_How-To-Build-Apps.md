title: "How To Build Apps Pragmatically"
-------------------------------
Recently, started I meta-analyzing how I build apps. I thought of best practices to ensure performance, user experience and quick development.
Here's what I found out:
##### Use Popular Tools
This one's controversial. 
But, you can't afford to waste time googling and opening Github issues. 
That's the reason why I use React and Django: both are tools with communities of millions and I never face problems with the language/framework itself: someone has done it for me before. 

##### Old Doesn't Mean Gold

Try to build a complex server-rendered web app with PHP because "It's more inclusive" or "it has better frontend performance". See you in 2030.

##### Use the Right Tool

Chose a tool because it's the right one - not because it's cool, users don't care whether the tech stack's cool.

Blogs using Javascript frameworks, I'm looking at you ;-)

If you're doing an app for developers, they'll prefer a CLI to a web app anyway.


##### Don't Duplicate Code

That helps to shrink complexity.
Try to regroup code that is always doing the same thing into a library with a clear interface.
For instance, all my web apps use the same extended fetching library that implements JWT authentication and pops up a warning whenever the backend receives an error code.

##### The Server and the Client Should not Mutate the Same Fields

It avoids errors from managing locks and synchronization mechanisms. 
If a background job can change some fields, note them as such and send them as read-only to the client. 
The client should only change "requested modifications" fields so that the background job does all the mutations.

##### Use Watcher Views
These are views that tell you when a model changed last. Watcher Views are light enough so that you can continuously call them to know whether you should fetch recent data. 
They're far less complex than WebSockets and avoid the performance costs of continuously polling unchanged data from the API.


##### Prefer Exposed to Hidden Complexity

Some solutions (e.g. serverless) promise you a short-term boost of productivity by not having to manage certain things. 
If you know that you will never have to manage these things, great! 
But if you know that you will need to get your hands dirty one day anyway, prefer exposed complexity from day one over hidden complexity that will force you to re-write everything when it appears.

<!--### Shrink Complexity
Obsess to minimize complexity: it's a balance to find. 


You need to think of the future. To design your app's data model so that you can support new features without changing it. 
It's not about adding more fields to your models, that would be increasing complexity: it's about adding more general and powerful fields. 
-->
##### Never Fit a Square Peg in a Round Hole
At Kaktana, we use nested Django models to represent a bot's trigger conditions. 
That's stupid! There's no point to storing function calls in a relational database: it is inefficient and complex. Whenever I want to add a microservice that needs to treat that state, I have to spend hours just building the JSON serializer.

When evaluating a solution, think of the tradeoffs you're making: are you adding complexity to get features you don't need?
In our case, we didn't think about it, and just implemented our conditions in the same way we stored products and their relations to merchands: in a relational database. 
It forced us to statically encode in the database model every needed combination of instruction, although what we needed was real programming, which is inherently dynamic.
We ended up with a very limiting set of instructions for our users that was hard to extend when needed.  

We should have made a Domain Specific Language (DSL) instead of our conditions. To serialize logic, we would just need to represent the AST in a lisp-like syntax. 
To interpret it on a new microservice, just create a tokenizer (10 lines of Python) and an AST interpreter.
We wouldn't have had to do anything to support more complex bots, as they would have just been a different code for our DSL.

This comes with experience, as you need to have seen a lot of ways of doing things to know the right one for your specific problem.  
Get out of your comfort zone and learn lisp! ;-)
