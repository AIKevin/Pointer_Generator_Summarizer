Pointer_Generator_Summarizer


The pointer generator is a deep neural network built for abstractive summarizations. 
For more informations on this model, you can check out the scientific article here: https://arxiv.org/pdf/1704.04368
You can also see this blog article from the author: http://www.abigailsee.com/2017/04/16/taming-rnns-for-better-summarization.html

With my collaborator Stephane Belemkoabga (https://github.com/steph1793) , we re-made this model in tensorflow for our research project. This neural net will be our baseline model.
We will do some experiments with this model, and propose a new architecture based on this one.

In this project, you can:
- train models
- test *
- evaluate *

* : for the test and evaluation, the main methods are not done yet, but we will release them very soon.

This project reads .bin format files. For our experiments, we will be working on the ccn and dailymail datasets.
You can download the preprocessed files with this link : 
https://github.com/JafferWilson/Process-Data-of-CNN-DailyMail

Or do the pre-processing by yourself with this link :
https://github.com/abisee/cnn-dailymail
