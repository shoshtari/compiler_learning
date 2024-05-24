grammar ExampleDSL;

start: program EOF;

program: output? hint initiate_game bomb_placements;

output:'output:' output_types ;

output_types: 'html' | 'console';

hint: 'hint:' hint_types;

hint_types: 'true' | 'false';

initiate_game: 'game:' width 'X' height;

width: INTEGER;

height: INTEGER;

bomb_placements: ('bomb:' bomb_location)+;

bomb_location: x_location ',' y_location;

x_location: INTEGER;

y_location: INTEGER;

INTEGER: '0' | [1-9]+ [0-9]*;

WS: [ \t\r]+ -> skip;
NEWLINE: ('\n' | '\r\n' | '\r') -> skip;

