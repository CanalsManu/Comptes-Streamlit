18/04/2026
- Acabar de transformar les dades actuals al nou format (db amd la convencio de les categories cat1-cat2 i del arbre cat-cat2-cat3)
- LLavors fer el update ala app daixo i mostrarcom es llegeixen les dades
- I tancar branch

- Gol actual es poder fer les MEVES propies comptes a la app directament, no cal posar massa mes coses fancies de moment

22/04/2026
- comptes.csv file created with
    - columns = (Data, Nom, Import, Categories, Classificació)
- columna classificació: arbre amb les possibles categories
- columna categories: categories de la classificació amb format cat-subcat-subsubcat-...
- added pages: 
    - add_movements: page where user will upload new movements and interactivelyclassify them
    - analysis: page with TABS, on each of this tabs some analysis
    - classification_tree: visualization of the current classification, and possibility to modify classification and re-classify some movements 
    - database: basic full database table
    - homepage: maybe has direct links to other pages, nice messages and its basic purpose is to trigger the initial dialog to update the comptes file
- future steps:
    - do add_movements pages: all the interactivity with the user
- small bug / feature: if you rerun while on a page which is not homepage, the dialog doesnt trigger

26/04/2026
DONE:
- do add_movements:
    - upload file
    - read it and make it a df
TODO:
- do add_movements:
    - dynamic part:
        - get new_movements from uplodaded_movements (compare)
        - dialog
            - shows movement info
                - day: coult be in calendar format (even google calendar) and even interactable to choose a day to jumpt o
                - name: possiblelink to google seach in new tab?
                - amount: color for positive or negative
            - shows
                - if unclassified: boxes with upper categories (already chosen despeses / ingressos based on amount)
                - if classified: classification
            - shows progress in classification (items done vs items todo)
            - shows buttons
                - left/right: move through all new movements (classificed and unclassified)
                - lleft/rright: (double arrows maybe) move through unclassified movements
                - erase current classification
                - close:
                    - if movements left to classify: close dialog without updating the db
                    - if no more movement left to classify: ask confirmation for updating db
                - auto?
        - upon clicking one box
            - either show more boxes with subcategories
            - save answer and jump to next movement to classify
            - if no more new movements left, show done and ask confirmation for updating db

27/04/2026
- I worked on comparing uploaded movements:
    - compare with pandas stuff
    - iteractively manage the controversial movements (TODO)
    - 'Nom'column shoudl be all upper
TODO:
- finish controversial
    - rember to clean the controversial_... in session state when closing
- do the plan from 26/04/2026

28/04/2026
- finished the controversial
    - open an closes with a flag on session
    - new gets the additions from controversial, on every run :( 
- next: start with classification 
- TODO: upload on new movements should not disappear when changing page

03/05/2026
- TODO: if controversial from movements are managed, and then the file is discarded and a new one uploaded, the controversial window doesn't appear. Bug -> fixed
- added progress bar, classification movement started
- NEXT: show appropriate classifications

07/05/2026
- Avoid rerunning in controversials
- Clasf tree from list/series
- TODO: start with classfication interaction

08/05/2026
- Updated description of _clsf_show_categories (check it out for plan)
- Started implenting it
- Also added basic interactino with buttons

09/05/2026
- Progress and badges added to clasf
- Added month to clsf

10/05/2026
- After clsf button -> move to next unclsf
- Added end page navigation button
- Plan:
    - plan end page <- DONE
    - do end page <- DONE
        - fancy stuff <- DONE
        - add result to movmeent <- TODO
        - maybe add buttons to show clsf in toggle end pageto jump to that page (?) 
        - maybe add highligh on sho clsf in toggle end page flagging undone (?)

11/05/2026
- Interactive table is too hard (either table with markdown or interactive dataframe)
- db now doesn't include classifition (that's on clsf_tree)
- Added movements to db
- Plan:
    - fix bug of disappearing uploaded_movements (after uploading movements, if page is changed, when returning to add movements page, the uploaded file will no longer be there)
        - while doing this, I got a weir error about parsing ett while compring bugs :((()))

16/05/2026
- Fixed bug of disappearing uploaded_movements, new keys added to session_state
- Possible plan ahead:
    - add 'auto' option. This has two flavors:
        1. get dict with known movements from db. Then, upon uploading new movements, compare new and known and ask what to do with them:
            - autocomplete all?
            - review autocompletion?
            - don't autocomplete?
        2. the other case is when user is classifying new movements and one such new movement appears repeated in the new movements:
            - ask if you want to autocomplete the rest?
            - or review them?
            - or don't do it?
        0. This autocomplete has to come with:
            - what happens when user changes classification? does that affect known movements? -> not really, cause db is only updated at the end
            - therefore, adding new movements to db should also update known movements
    - save and exit option:
        - meaning, save and download the current db + classifciation tree into a csv file
            - maybe csv should include some metadata like, creation date?
        - button maybe at the bottom of sidebar? or maybe at bottom right corner? always present
        - is there a way to ask user to confirm before leaving page, and also offer to save current progress
    - some basic analysis
        - tables per month
        - dynamic plot (save plot info so user defines custom plots?)

18/05/2026
- added download button to download db and clsf_tree
- correct names to pages
- couple of big fixes:
    1. homepage now is default after refresh
    2. month name quick fix
- Plan:
    1. autocomplete from 16/05/2026
    2. use it with real movements
    3. basic analysis

28/05/2026
- About autocomplete 1 (comparing to db):
    - A window should pop up right after controversials are handled (if known movements are found)
    - It should say that known movements were found and ask what to do
        1. autocomplete all
        2. review autocomplete
        3. skip
    - Maybe better to only offer
        1. autocomplete all
        2. skip
        0. show known movements found
- So, in the middle of autcomplete implementation:
    - we have known
    - we are comparing them
    - now we just have to ask user what to do and show found known movements
    - if autocomplete -> how to autocomplete?
        - pass it to classify movement maybe?
        - or keep it in sepearate df and when db is updated update those too? <- this looks better

01/06/2026
- Added ss = st.session_state in many places ot keep the code tidy
- Continue autocomplete:
    - "Known items found"
    - Autocomplete & Ignora
    - Show known found
- DONE:
    - autocomplete flavour 1
    - added tab option to show and hide display
- TODO? Add autocomplete on final display of classification too?
- NEXT:
     - autocomplete flavour 2: autocomplete rest of movements as you are classifying

03/06/2026
- POSSIBLE TASKS:
    - clean homepage after uploading comptes
        - show links to other pages in nice layout
        - offer the option to change comptes file? -> care with the cleanup this requires
    - name of the downloaded file (DONE)

- BUG: pressing ENTER clicks whatever is selected in the browser
    - possible fix: make and hide a button bound to ENTER
    - on autocomplete the background has comença classificació with bind enter, so it triggers that button from the autocomplete dialog
    - I tihnk this is the general issue (also in other states): that enter triggers the background button
    - fix then?
        - unbind?
        - find and rebind based on dialog windows being open?
        - fixed the one with autocomplete, but now the blinking is still there...
        - slowly getting there... figure out what is getting called when you press enter

04/06/2026
- ON THE BUG of enter:
    - when ENTER is bound somewhere, the focused item is not clicked. When enter is not bound, the focused item is clicked.
    - separately, having a dialog open and clicking a background button with shortcut (enter) closes the dialog -> CONFIRMED with dummy button on the backgroudn shortcut to 8 (doesn't work for the autocomplete dialog)
    - maybe clicking with shortcut outisde of dialog only closes dialog when dialog is dissmissable
    - also triggering background button triggers rerun of the whole thing
    - maybe the blinking issue comes from the dialog being opeend from two different lines
    - so, i have two issues here:
        1. clicking a background button with shortcut while dialog is opened closes the dialog
        2. focused items when enter is unbound are clicked with enter (apparently dosen't apply to toggles)

- BUG FIXED. Lessons learned:
    1. On blinking and vackground clicks
    - background button click (with shortcut) forces rerun
        - dialog not closed automatically (regardless of dismissable)
        - dialog closed based on effects of rerun
    - dialog blinked because on rerun it was opened from ANOTHER line (another call to classify_movements())
    - SOLUTION (for clasf): open the dialog from the same call
    - SOLUTION (for auto): bind to enter autocomplete + unbind the one to comença... 

    2. On binding enter
    - if enter is not bound to anything, it clicks on the focused item
    - this can click random buttons you do not want (like close button)
    - SOLUTION: have it bound to something (we have it bind to the background one)