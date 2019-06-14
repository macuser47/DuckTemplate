# Ducks #
This readme exists to answer the question on your mind right now:

## What the fuck is a Duck? ##
A duck is a type of template that acts like a fillable form.
Suppose you have a templated file that you want to insert instance-specific
strings into. Ducks enable you to denote which parts of the file to fill in, and
what prompts to give the user to populate them.

For example, the following duck will produce the below configuration queries:

### Duck ###
```
The quick {<What color do you want?>} fox jumped over the lazy 
{<What kind of animals do you want?>}.  
```

### Result ###
```
What color do you want? brown
What kind of animals do you want? dogs
```

The template would then produce the following file:

```
The quick brown fox jumped over the lazy dogs.
```

This applies to any file put into the ducks folder. Each file will create a
user input session and the generated files will be placed in the root directory of the template instance.


## Specification ##

User fillable fields are denoted as 1 or multi-line annotations
starting with `{<` and ending with `>}`. Fillable fields may not contain the starting or ending marker.

The space inside the field can denote the user input query and/or the id associated with the field. 
Field ids are used in cases where a single input should fill multiple locations the document.

Ids are denoted at the start of the field, followed by a colon.
Any text that follows is considered part of the user input query.

```
{<id:input query>}
```

In the following example, a single query is used to populate a value
with id "target" to several fields.

```
cd {<target:What is the target directory?>}
cp -r ~/some/dir {<target:>}
chmod -R user:user {<target:>}
```

Note that both id and query values are optional, but an annotation defining
only an id will case an error if a query string was not previously
defined for the id.
