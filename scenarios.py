"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of my five criteria needs something run against it, and this file is where
I wrote down what. `run_eval.py` runs everything here three times.

One thing this file cannot do, and it is worth saying at the top rather than
burying it. `run_eval.py` only talks to `/submit`. Two of my criteria are not
about `/submit`:

  - **Criterion 4** is about the appeal path, which needs a submission first
    and then an appeal against the content_id that came back.
  - **Criterion 5** has a timing bound in it (nothing over 10 seconds), and
    `run_eval.py` records status codes but not durations.

So I extended the tooling rather than testing those two by hand. They are in
`run_extra_checks.py`, which does the same three trials and writes its own
results file. The status code half of criterion 5 is still here, because that
part a "bodies" scenario can express perfectly well.
"""

# ─── Criterion 1: my own writing ─────────────────────────────────────────────
#
# ⚠️ THIS IS THE ONE THAT HAS TO BE MINE.
#
# Criterion 1 says "of 10 pieces of writing that I wrote myself, at most 1
# comes back with a guess of ai". Somebody else's prose cannot test that. It
# would not be my false positive rate, it would be theirs, and the number it
# produced would mean nothing about my own writing on my own service.
#
# Ten pieces, each a paragraph or so. Things I actually wrote: posts, notes,
# messages, bits of old essays. Plain everyday writing is better here than my
# best writing, because plain writing is what my service accuses.
#
# ⚠️ WHAT THIS SAMPLE ACTUALLY IS, because the number is only worth what the
# sample is worth.
#
# These ten pieces are not ten separate things I wrote. They are one document
# cut into ten paragraph sized chunks: a case study review I wrote for a data
# science module, on storytelling and narratives in data science. One topic,
# one register, one sitting.
#
# That matters when reading the result. Criterion 1 says "10 pieces of writing
# that I wrote myself", and these are mine, but they test my formal academic
# writing rather than my writing in general. Ten chunks of one essay cannot
# disagree with each other the way ten genuinely separate pieces would.
#
# It is still the right sample to start with, and not only because it is what I
# had. The attack set's false_positive family aims at exactly this register:
# FP04 is "a student essay written to a rubric" and FP02 is "human writing in a
# formal register". My service accused both. So this is my own writing in the
# register that already broke it.
#
# Everything below is exactly as I typed it, including the typos. Correcting
# them would change what the detector sees, which is the one thing I must not
# do to this sample.
MY_OWN_WRITING = [
    # 1.
    "The team presented the topic on Storytelling and narratives in data "
    "science. They clearly started from how story telling is important in our "
    "day-to-day life and then transitioning to how its important from a data "
    "science perspective. The topic is essentially how data visualization "
    "plays a critical role and how it needs to be self-explanatory. The topic "
    "also explores how visualization has moved on from simple plots to data "
    "exploration and analysis.",

    # 2.
    "The topic goes on to explore common steps involved in coming up with "
    "good data visualization and story-telling ranging from genre, visual "
    "tactics and narrative tactics. And what makes a good data story. The "
    "topic validity was confirmed by three separate papers (2010 narrative "
    "visualization, 2013 storytelling: the next step, 2015 more than telling "
    "a story) that the team worked on which all came to the same conclusion "
    "on how tools are meant to use for telling a good data story and what "
    "constitutes them.",

    # 3.
    "The topic covered both good and bad examples on telling a story on data "
    "using visual plots about world population and budget forecasts. The "
    "topic explains how visualization was born explanatory. That the "
    "presentation is not a new problem that visualization has yet to solve, "
    "it is the original problem and the field drifted away from it toward "
    "exploration and analysis. The topic explains how matching the technique "
    "to the setting is a design decision not a detail.",

    # 4.
    "The topic really matters as the end viewer can range from a normal "
    "person who might not fully understand what the data or visualization "
    "stands for. The presentation clearly mentioned a criticial insight about "
    "the gap between the analyst and the decision maker. As evident the "
    "analyst will be the person responsible for exploring the data followed "
    "by proper presentation. But the decision makers often need not have "
    "sound knowledge on how to interpret the data.",

    # 5.
    "An inaccurate or often not well annotated data visualization might throw "
    "off the interpretability for the final decision maker, even leading to "
    "wrong decisions being taken. And wrong decisions can cost on several "
    "accounts ranging from money, life, consequences to name a few.",

    # 6.
    "Hence the data visualizations should be self-explanatory and can even be "
    "structured in a way that it tells a story (for example a growing trend "
    "of pollution and what mitigation steps can be taken by the concerned "
    "authorities). In a world where every decision is now data driven, the "
    "need for a well sounded data visualization and practices is of the "
    "utmost importance.",

    # 7.
    "I would give them an A grade. I loved how the presentation started by "
    "laying out how visualization is important. And then slowly transitioning "
    "it into how its important from a data science stand point. I loved how "
    "the presentation was well structured. How they pointed out three "
    "different papers they looked into and how they all come about to a "
    "similar conclusion on how visualization matters in telling the stories "
    "right.",

    # 8.
    "I liked their responses to the questions asked at the end of the "
    "presentation. I did feel that they could’ve simplified couple of the "
    "example slides to make it less content heavy. But overall it was a good "
    "effort, the topic was clearly conveyed with sufficient examples and "
    "visual slides and the right amount of facts and supporting arguments "
    "sticking to the time constraint for presentation.",

    # 9.
    "From the presentation I was able to take away several key points. First "
    "and the foremost how visualization is very important in real life. How "
    "the visualization tells a story and not just spit out data. How "
    "visualizations need to be self-explanatory to the audience. I was also "
    "able to learn how visualizations have grown from simple plots to now "
    "exploring the data exploration and analysis. Order, connection and "
    "guidance are what turn a visualization into a story. Best practices to "
    "follow while trying to tell the story through visualizations. Some "
    "examples of what a failed visualizations looks like vs what a successful "
    "visualization looks like.",

    # 10.
    "The common steps involved in coming up with a good visualization "
    "starting with 1. Genre (and the 7 building blocks), 2. Visual tactics "
    "(visual structuring, highlighting, transition guidance), 3. Narrative "
    "tactics (ordering: linear, random, access, or user-directed; "
    "interactivity and critically how the user learns it-explicit "
    "instruction. The three parts that make a good data story: 1. Story "
    "pieces (facts backed by data interpretation is left to the viewer), 2. A "
    "clear message (annotation states what the viewer is meant to take away), "
    "3. Meaningful order (pieces connected in sequence, building to a "
    "conclusion). One critical insight involved how there is a gap between "
    "the person who analyses the data and the one who finally makes a "
    "decision.",
]


# ─── Criterion 2: do clearly AI and clearly human writing separate? ──────────
#
# My criterion asks for the AI group to average at least 0.30 above the human
# group. 0.30 is the width of my unsure band, and the argument is that if the
# two kinds of writing do not separate by at least the width of the band I
# claim to be measuring, my thresholds are decoration.
#
# Two scenarios rather than one list of six, so I can read the two group
# averages straight off the output instead of remembering which rows were
# which.
#
# Being honest about what these are: the "clearly AI" three are generated
# prose, and the "clearly human" three I wrote. Neither group is a sample of
# anything. Three and three is a small enough number that one odd text moves
# the average, which is part of why I am measuring group averages rather than
# demanding every AI piece beat every human piece.

CLEARLY_AI = [
    "The implementation of this feature requires careful consideration of "
    "several important factors. It is essential to note that the system must "
    "be able to handle a wide variety of different use cases. Additionally, "
    "the overall performance of the solution depends on a number of key "
    "variables. In conclusion, a thorough approach is recommended.",

    "Effective communication in the workplace is widely recognised as a key "
    "driver of organisational success. Teams that communicate clearly are "
    "better positioned to meet their objectives and to respond to changing "
    "circumstances. Furthermore, a culture of open dialogue contributes to "
    "improved employee engagement and overall job satisfaction.",

    "There are several important benefits to maintaining a regular exercise "
    "routine. First and foremost, physical activity has been shown to improve "
    "cardiovascular health. In addition, regular exercise can help to reduce "
    "stress levels and improve the quality of sleep. Finally, it is worth "
    "noting that consistency is more important than intensity.",
]

CLEARLY_HUMAN = [
    "My bike chain snapped two miles from home, in the rain, outside a shut "
    "pub. I walked it back. Halfway there a man in a Vauxhall slowed down, "
    "looked at me, and drove off. Fine. Great. I have since bought a chain "
    "tool and I carry it everywhere, including to work, where there is no "
    "bike.",

    "The cat has decided the printer is hers now. Not the top of it. Inside "
    "it, somehow, through the paper tray, which I did not think was possible "
    "and which the manual does not cover. I have stopped printing things. It "
    "seemed easier than the alternative, which was explaining this to a "
    "repair shop.",

    "We got to the campsite about four and the pitch was on a slope, which "
    "nobody mentioned in the listing. Put the tent up anyway. Woke at two in "
    "the corner of it with all the bedding on top of me like a very slow "
    "landslide. Dad called this character building. It was not.",
]


# ─── Criterion 3: are all three labels reachable? ────────────────────────────
#
# These are the five calibration texts from unit 7 milestone 4, plus one more,
# so I can compare against the numbers already written up in notes.md. Unit 7
# had them landing at 0.1928, 0.4778, 0.4920, 0.7110 and 0.8151, which covers
# all three labels. If one of my three labels has stopped being reachable, this
# is where I find out.

LABEL_COVERAGE = [
    # unit 7: 0.1928, high confidence human
    "My bike chain snapped two miles from home, in the rain, outside a shut "
    "pub. I walked it back. Halfway there a man in a Vauxhall slowed down, "
    "looked at me, and drove off. Fine. Great. I have since bought a chain "
    "tool and I carry it everywhere, including to work, where there is no "
    "bike.",

    # unit 7: 0.4778, unsure
    "The Committee convened on the fourteenth of March to consider the "
    "proposed amendment to Article 7, which had been tabled by the delegation "
    "from Lisbon some weeks earlier. Objections were raised on procedural "
    "grounds; these were noted, debated at length, and ultimately set aside. "
    "The amendment carried by a margin of three votes.",

    # unit 7: 0.4920, unsure. AI text with typos and chopped sentences
    "The implementaton of this feature requires careful consideration. Of "
    "several important factors. It is essential to note that the system must "
    "be able to handle a wide variety of diffrent use cases! Additionally the "
    "overall performance of the solution depends on a number of key "
    "variables, In conclusion a thorough approach is recomended.",

    # unit 7: 0.7110, high confidence AI
    "The implementation of this feature requires careful consideration of "
    "several important factors. It is essential to note that the system must "
    "be able to handle a wide variety of different use cases. Additionally, "
    "the overall performance of the solution depends on a number of key "
    "variables. In conclusion, a thorough approach is recommended.",

    # unit 7: 0.8151, high confidence AI. Plain human writing, and the case
    # my whole unit 7 write up is about.
    "To fix a bike chain you need a chain tool. First you must find the "
    "broken link. Then you push the pin out with the tool. After that you can "
    "remove the bad link. Then you join the two ends together again. It is "
    "not hard but you need the right tool.",

    # The sixth. Genuinely borderline on purpose: a person writing plainly
    # about something specific, with a little bit of voice in it.
    "The boiler makes a noise now. Not a bad noise, I think, more of a knock "
    "about twice a minute when the heating comes on. I looked it up and the "
    "internet says it is either nothing at all or the whole thing needs "
    "replacing. I have decided to believe the first one until about November.",
]


SCENARIOS = [
    {
        "name": "clearly AI",
        "criterion": 2,
        "texts": CLEARLY_AI,
    },
    {
        "name": "clearly human",
        "criterion": 2,
        "texts": CLEARLY_HUMAN,
    },
    {
        "name": "label coverage",
        "criterion": 3,
        "texts": LABEL_COVERAGE,
    },
    {
        # Criterion 5's status code half. The timing half is in
        # run_extra_checks.py, because run_eval.py does not record durations.
        #
        # These are raw request bodies rather than strings, because "the text
        # field is missing" and "the text field is null" are things a string
        # cannot say.
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"creator_id": "eval_bad_missing"},                      # no text key
            {"text": "", "creator_id": "eval_bad_empty"},            # empty
            {"text": None, "creator_id": "eval_bad_null"},           # null
            {"text": "word " * 50000, "creator_id": "eval_bad_huge"},  # enormous
        ],
    },
]

# Criterion 1 only runs once I have put my own writing in the list above.
# Leaving it out of the run is better than running it against somebody else's
# prose and writing down a false positive rate that is not mine.
if MY_OWN_WRITING:
    SCENARIOS.insert(0, {
        "name": "my own writing",
        "criterion": 1,
        "texts": MY_OWN_WRITING,
    })


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
