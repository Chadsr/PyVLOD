# Voting Linked Open Data (V-LOD)

Using LD-R

## Installation

    # Requirements: Linux with stardog 4.2 installed
    
    cd ~
    sudo apt-get install git
    git clone https://github.com/SW-g16/sw.git
    sudo sh sw/scripts/install.sh
    # yes to all prompts

## Running

    sh sw/scripts/start.sh

## Checking 

There should be stuff at localhost:5820 and localhost:3000. 
If you've run start.sh and said yes to the last two prompts, 
you should see some data in localhost:3000->datasets->\[...\]votes\[...\]

## About

This is a project revolving around the semantic organization and
presentation of voting data from different endpoints.

## Choice of framework

 - Lets us use existing ui components for semantic data
 - If we produce a useful application, it will be easier for others to reuse it
 - LD-R is generally awesome

## Status, considerations, design notes

These are things and decisions that need to done and taken

### Ontology

A minimal voting ontology is given as `ontology.ttl` upon initial commit.
It tells us that Voters abstain or vote yay or nay to Bills.
This can be expanded both for Bills and Voters.
Voters can belong to parties, bills, have dates, etc

### Inference

LD-R displays Stardog's inferred knowledge that v:bob is a owl:Thing.
Woo!

### Deduction

We want to deduce plotable numbers of interest from our dataset.
This can (should?) be done with sparql.

### Data Flow

Store copies of external data or query external data in real-time?

### Visualization

look for existing ld-r components for visualization.
if we don't find what we want, we can make some
within the ld-r framework.

What do we want to visualize exactly, and how?

 - network graphs (of what?)
 - plots (statistics over time)

look for visualizations of other political data for inspiration

### Data acquisition

Endpoints arent uniform. This is among the problems of web 2.0 and motivation for semantic web.
We'll need to do some custom coding for new endpoints.
Different endpoints have different numbers of timbl-stars.
We are very happy when states provide 5-star data
 - particularly if the 5th star is earned by using a shared vocabulary for votes.
This would let us use access several datasets with a single alignment.
In less fortunate cases, we get 3-star data.
We can still construct rdf data with json and csv, but we won't go lower.
