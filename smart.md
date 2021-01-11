# smart solver
<!-- .element: class="fragment  highlight-blue" --> 

## flow free
---n

## main components
* Forward checking ​
* MRV (minimum remaining value)​
* Degree heuristic​
* Least constraining value​
---n

<!-- .slide: data-auto-animate -->
## variable domain 
* forward checking
* MRV (minimum remaining value)
--v

<!-- .slide: data-auto-animate -->
## variable domain
![domain in 5x5 table](images/5x5_domain.png)

example in 5x5
--v

## variable domain
code implementation 
```js [1|4|7,8|9]
full_domain = colors

point_domain = []
for value in full_domain:

    assignments[coord] = value
    if is_consistant(initial_state, {coord: value},
                    assignments, inp, connected_terminals):
        point_domain += value
    del assignments[coord]

return point_domain
```
--v
<!-- TODO use r-stack -->
<!-- .slide:  data-transition="none" -->
## variable domain    
example 

![](images/5x5_with_domain.png)
<!-- .element class="r-stretch" -->
--v

<!-- .slide:  data-transition="none" -->
## variable domain    
example 

![](images/choose_first.png)
<!-- .element class="r-stretch" -->
--v

<!-- .slide:  data-transition="none" -->
## variable domain    
example 

![](images/5x5_selected_box.png)
<!-- .element class="r-stretch" -->
--v

<!-- .slide:  data-transition="none" -->
## variable domain    
example 

![](images/choose_second.png)
<!-- .element class="r-stretch" -->
---n

# forward checking 
* find domain for variables
* if variable has zero domain 
* return case failure
--v

## forward checking 
```python [|3]
def forward_check(variables_domain):
    for coords in variables_domain:
        if len(variables_domain[coords]) == 0:
            return False
    return True
```
--v

<!-- .slide: data-auto-animate -->
## results
* without forward_check
  | map​ | time​ | Number of hits​ |
  |------|-------|-----------------|
  | 5x5​ | 7 ms​ | 443             |
--v

<!-- .slide: data-auto-animate -->
## results
* without forward_check
  | map​ | time​ | Number of hits​ |
  |------|-------|-----------------|
  | 5x5​ | 7 ms​ | 443 <!-- .element: class="fragment  highlight-red" -->            |


* with forward_check
 <!-- .element: style="margin-top:100px" -->
  | map​ | time​ | Number of hits​ |
  |------|-------|-----------------|
  | 5x5​ | 9 ms​ | 28​ <!-- .element: class="fragment  highlight-blue" -->             |
---n

<!-- .slide: data-auto-animate -->
# MRV
* find domain for variables
* choose variables with smallest domain
--v

<!-- .slide: data-auto-animate -->
# MRV
* implementation
```python [1-2|3|5|9,10]
    smallest_domain = math.inf
    selected_coords = []
    for coord in variables_domain:
        domain_len = len(variables_domain[coord])
        if domain_len < smallest_domain:
            selected_coords = []
            smallest_domain = domain_len

        if smallest_domain == domain_len:
            selected_coords.append(coord)

    return selected_coords
```
--v

<!-- .slide: data-auto-animate -->
# MRV
applying to 5x5

![](images/mrv_5x5.png)
<!-- .element class="r-stretch" -->
--v

<!-- .slide: data-auto-animate -->
# MRV
applying to 5x5

![](images/mrv_5x5_select.png)
<!-- .element class="r-stretch" -->
--v

#### results *
<!-- https://github.com/A-Siam/FlowFree/pull/2 -->
| map  | time (s) |
| ---- | -------- |
| 7x7  |  1.87    |
| 8x8  |  1.73    |
| 9x9  |  6.87    |
| 10x10  |  ?.??    |


--v
<!-- .slide: data-auto-animate -->
### limitation
* variable domain calculation increase with map size

  * example 
<!-- .element: class="fragment" -->
    * 14x14 every time caluclate domain <br/>
      for (<span class="fragment highlight-blue">196 </span> -  terminals) variable
  * solution
<!-- .element: class="fragment" -->
    * update only constrained varialbes
--v
<!-- .slide: data-auto-animate -->
### limitation
* variable domain calculation increase with map size
  
* consistency check represent the bottleneck
  * <span class="fragment"> check <span class="fragment highlight-blue">profile </span>analysis and improve as possible </span>

  
---n
# optimization
<!-- .element: class="r-fit-text" -->
--v

<!-- https://github.com/A-Siam/FlowFree/pull/7 -->
<!-- .slide: data-auto-animate -->
### improvement in constrains
profile for 991
![](images/bad_constrain.png)

<span> terminal constrain was checking <span class="fragment highlight-red"> every </span>terminal has only on path </span>
--v
<!-- .slide: data-auto-animate -->
### improvement in constrains
profile for 991
![](images/good_constrain.png)

<span> check only <span class="fragment highlight-blue"> neighbor </span> terminals </span>
--v

#### results
<!-- https://github.com/A-Siam/FlowFree/pull/2 -->
| map  | time (s) |
| ---- | -------- |
| 7x7  |  0.085    |
| 8x8  |  0.157    |
| 9x9  |  0.858    |
| 10x10(1)  |  3.300    |
| 10x10(2)  |  1.680    |
| 12x12  |  14.971    |
| 12x14  |  ??.???    |
<!-- .element: class="r-stretch" -->
--v

<!-- .slide: data-auto-animate -->
### dynamic domain-upgrade

* save variable domain
* only update constrained variables
--v

<!-- .slide: data-auto-animate -->
### dynamic domain-upgrade

* the constrained variables

  * are variables who share constrain with last updated variable

--v

<!-- .slide: data-auto-animate -->
### dynamic domain-upgrade

* the constrained variables

  *  are empty neighbor </span> <span class="fragment highlight-blue"> (point good combination) 
--v
<!-- .slide: data-auto-animate -->
### dynamic domain-upgrade

* the constrained variables

![](images/5x5_constrained_add.svg)

--v
<!-- .slide: data-auto-animate -->
### dynamic domain-upgrade

* the constrained variables

![](images/5x5_constrained.svg)

--v

<!-- .slide: data-auto-animate -->
### dynamic domain-upgrade

* the constrained variables
  
  * are empty neighbor (point good combination) 
  * are empty neighbor for occupied neighbor 
  
    <span class="fragment highlight-blue"> (neighbors/terminal good combination) </span>

--v
<!-- .slide: data-auto-animate -->
### dynamic domain-upgrade

* the constrained variables

![](images/5x5_constrained_2_add.svg)

--v

<!-- .slide: data-auto-animate -->
### dynamic domain-upgrade

* the constrained variables

![](images/5x5_constrained_2.svg)

--v
<!-- .slide: data-auto-animate -->
### dynamic domain-upgrade

* the constrained variables
  *  are empty neighbor  (point good combination) 
  * are empty neighbor for occupied neighbor 
  
    (point neighbors/terminal combination)
  * every point when terminal is connected <span class="fragment highlight-blue"> (terminal connected) </span>

--v
### dynamic domain-upgrade
implementation
```python [2|5,6|11,12|13|14]
variables_domain = {}
connection_changed = len(connected_terminals)>len(prev_connected_terminal)
first_run = prev_variable == None
if connection_changed or first_run:
    # update all variables
    for coord in variables:
        domain = get_available_domain(coord,
        assignments,connected_terminals)
        variables_domain[coord] = domain
else:
    variables_domain = pickle.loads(pickle.dumps(prev_domain))
    del variables_domain[prev_variable]
    big_neighbors = get_constrained_neighbors(prev_variable,inp,assignments )
    for coord in big_neighbors:
        domain = get_available_domain(coord, assignments, inp,connected_terminals)
        variables_domain[coord] = domain
return variables_domain
```
<!-- .element: class="r-stretch" -->

--v
<style>
    #result_table > tbody > tr >td {
        font-size: 25px;
    }

</style>
#### results
| map​       | time​    | Number of hits​ |
|------------|----------|-----------------|
| 5x5​       | 6 ms​    | 17​             |
| 7x7​       | 16ms​    | 41​             |
| 8x8​       | 30 ms​   | 52​             |
| 9x9 (1)​   | 57ms​    | 67​             |
| 10x10 (1)​ | 189ms​   | 320​            |
| 10x10(2)​  | 93ms​    | 139​            |
| 12x12​     | 290ms​   | 331​            |
| 12x14​     | 193ms​   | 148​            |
| 14x14​     | 78750ms​ | 10309​          |
<!-- .element: class="r-stretch" id="result_table"-->
---n

## degree heuristic
- explain
- relation to constrained variables
--v

### results
- blaim implementaion
- we will get better without it
---n

## least constraing value
- explain
--v

#### result 
--v

### special credit for 1414
- explain the initial choice
---