# extractive_text_summerization
Extractive text summerization using multinomail Naves bayes classifier
To understand multinomail Naves bayes classifier watch https://youtu.be/OWGVQfuvNMk
IN dataset,
there are sentences with value 0 or 1 
which means
if that sentence is used for summerization then has value 1 
if not used for summerization then has value 0.
which means dataset has two classes 1-yes class , 0-no class.
IN code,
we find prior probablities of two classes and assign it to yes_prior and no_prior.
condition probablities of all words all included in features dictionary.
feauter['yesfeauter] --- dict for conditional probablity for all bag of words for class 1 or yes.
feauter['nofeauter] --- dict for conditional probablity for all bag of words for class 0 or no.
for finding summery for given text document,
iterate through sentence 1 by 1 ,
create bag of words preprocessed words of that sentence,
multiply conditional probablity of all words with prior probablity for both classes in yes variable and no variable.
check if posterior probablity of two class if yes>no
append to summery 
else go to next line 
evalute the summery using rouge 
the reference summery taken from online text summerizer.
