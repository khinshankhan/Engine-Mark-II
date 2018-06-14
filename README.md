# G4Lyfe_Engine-Mark-II

### By Khinshan Khan (Period 10)

#### The following outlines the features I implemented beyond the course requirements:

## Color constants

#### An idea revised from the MDL.spec about `constants`. Instead of the user having to enter like 9 digits per constant, I have pre-made ones, that the user need not define:

`[black, white, red, green, blue, pink, yellow, cyan, coolyellow, coolblue, coolpink]`

#### These should be used similarly to how constants were described in the spec file:

`mesh <color>:skyscraper.obj`

#### where `<color>` is one of the names from the array

#### DISCLAIMER: The user can still create constants as outlined in the spec file, however, I do some crazy math so I can't gurantee it'll be even remotely as they hoped the color would turn out (most tend to become white actually). In addition, the user shouldn't try to make a new constant with the same name as in the array (so far, it doesn't break, but some weird color stuff happens)

## Meshes

#### As outlined in the MDL.spec file, user has to put the `.obj` file in the `obj_files/` directory. They can then call the `.obj` in an `.mdl` script as:

`mesh <color>:mini_cooper.obj`

#### where `<color>` is the previous feature, but it can just be left blank and default coloring (ehich is greenish blue, think back to the old assignments) will be used.

#### DISCLAIMER: Only deals with `v` and `f` lines, ignores the rest (ie I don't bother with vertex normals nor textures, etcetera)

## Important Notes

### Not Features, But Important Notes:

#### Changed directory to make it neater/ organized. The `.mdl` scripts should now be in the `inputs/` directory.

#### Because of the previous change, user can now run script files either using the `makefile` commands or by running `python main.py <filename>.mdl` or `python main.py mdl/<filename>.mdl` (`makefile` takes both variants as well).
