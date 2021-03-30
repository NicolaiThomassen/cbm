# Contributing to CbM

Please take a moment to review this document in order to make the contribution
process easy and effective for everyone involved.

Following these guidelines helps to communicate that you respect the time of
the developers managing and developing this open source project. In return,
they should reciprocate that respect in addressing your issue or assessing
patches and features.


## Using the issue tracker

The [issue tracker](https://github.com/ec-jrc/cbm/issues) is
the preferred channel for submitting [pull requests](#pull-requests) and
[bug reports](#bugs), but please respect the following
restrictions:

* Please **do not** use the issue tracker for personal support requests. Please
  consider one of the following alternatives instead:
  * [JRC GTCAP Wikis platform](https://webgate.ec.europa.eu/fpfis/wikis/display/GTCAP/GTCAP+Home)
  for Q&A as well as support for troubleshooting, installation and debugging. Do
  remember to tag your questions with the tag `cbm`.
  * [Contact directly JRC GTCAP team](https://marswiki.jrc.ec.europa.eu/wikicap/index.php/Main_Page)

<!--
  * Mailing list: The [CbM JRC Group](https://---/forum/#!forum/cbm)
-->


## Pull requests

Good pull requests - patches, improvements, new features - are helpful.
They should remain focused in scope and avoid containing unrelated commits.

**Please ask first** before embarking on any significant pull request (e.g.
implementing features, refactoring code), otherwise you risk spending a lot of
time working on something that the project's developers might not want to merge
into the project. Please read the [tutorial on writing new CbM functions](https://jrc-cbm.readthedocs.io/en/latest/dev_developing.html)
if you want to contribute a brand new feature.

If you are new to Git, GitHub, or contributing to an open-source project, you
may want to consult our [guide on preparing and submitting a pull request](https://jrc-cbm.readthedocs.io/en/latest/dev_pull_request.html)
or check our list of [useful related documentations](https://jrc-cbm.readthedocs.io/en/latest/dev_learn.html).


<!--
### Checklist

Please use the following checklist to make sure that your contribution is well
prepared for merging into the main CbM repository:

1. Source code adheres to the coding conventions described in [CbM Style Guide](https://jrc-cbm.readthedocs.io/en/latest/dev_style_guide.html).
   But if you modify existing code, do not change/fix style in the lines that
   are not related to your contribution.

2. Commit history is tidy (no merge commits, commits are [squashed](http://davidwalsh.name/squash-commits-git)
   into logical units).

3. Each contributed file has a [license](#license) link on top.
-->


## Bug reports

A bug is a _demonstrable problem_ that is caused by the code in the repository.
Good bug reports are extremely helpful - thank you!

Guidelines for bug reports:

1. **Check if the issue has been reported** &mdash; use GitHub issue search and
   mailing list archive search.

2. **Check if the issue has been fixed** &mdash; try to reproduce it using the
   latest `main` branch in the repository.

3. **Isolate the problem** &mdash; ideally create a reduced test
   case.

A good bug report shouldn't leave others needing to chase you up for more
information. Please try to be as detailed as possible in your report. What is
your environment? What steps will reproduce the issue? What would you expect to
be the outcome? All these details will help people to fix any potential bugs.

Example:

> Short and descriptive example bug report title
>
> A summary of the issue and the OS environment in which it occurs. If
> suitable, include the steps required to reproduce the bug.
>
> 1. This is the first step
> 2. This is the second step
> 3. Further steps, etc.
>
> Any other information you want to share that is relevant to the issue being
> reported. This might include the lines of code that you have identified as
> causing the bug, and potential solutions (and your opinions on their
> merits).


## License

CbM is [3-Clause BSD licensed](https://github.com/ec-jrc/cbm/blob/main/LICENSE), and by submitting a patch, you agree to
allow Open Perception, Inc. to license your work under the terms of the BSD 3-Clause
License. The link of the license should be inserted as a comment on top
of each `.py` file e.g.:

```py
# This file is part of CbM (https://github.com/ec-jrc/cbm).
# Copyright : 2021 European Commission, Joint Research Centre
# License   : 3-Clause BSD
```

Please note that if the academic institution or company you are affiliated with
does not allow to give up the rights, you should contact us for further details.
