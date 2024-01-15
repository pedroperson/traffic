# Traffic

download the repo and run main.py

it works on my computer :)

- Labeenus

## Git

Just a recap:

1- when you open this project in your computer, always run

```
# Get up-to-date code from repo
git pull origin main

# Create a new branch to start making your changes
git checkout -b your_branch_name
```

2- Do your changes
3- Add changes to the context and commit them as you go

```
git add .
git commit -m "a descriptive sentence or two of the changes you are commiting"
```

4- push your work to the repo (you may have to git pull again/ rebase if someoned pushed since you last pulled)

```
git push origin main
```

## Formating

I am using the "Black Formatter" extension in VS code to autoformat onsave. Lets use the default settings for now.

## TODOs

- write display logic
- write better versions of the functions at the bottom of map.py
- write the map controller
- remove the map knowdge for the car class -> I tried to do this but it requires a higher level of abstraction we dont have yet

- test vertical only
