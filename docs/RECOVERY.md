# Recovery provenance

No untouched original source archive was available when publication was requested.
The source text was recovered separately by reversing recorded edits and using
captured pre-edit file reads. Eighteen recovered files matched pre-edit contents;
the model service's Python syntax tree also matched its pre-edit read. The remaining
recorded source edits were reversed. Original byte-level newline and JSON formatting
cannot be certified, so this repository is labelled a recovered original.

The preserved model bundle was copied byte for byte, with matching SHA-256 hashes.
It loads in real inference mode with 22 metadata fields and 77 encoded features.
All 26 recovered Python files parsed successfully. The original evaluation and app
preprocessing are distinct; their performance should not be conflated.

The first source commit is tagged `recovered-original-source`. Later publication
changes add setup notes, aggregate results, provenance, CI and ignore rules. They
do not change the recovered Python/JavaScript application or training code.
The [recovery manifest](recovery_manifest.json) records source and bundle hashes.
Private session transcripts, local filesystem paths and per-patient rows are not
part of this publication.
