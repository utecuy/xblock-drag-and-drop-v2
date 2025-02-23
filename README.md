Drag and Drop XBlock v2
=======================

This XBlock implements a friendly drag-and-drop style problem, where
the learner has to drag items to zones on a target image.

The editor is fully guided. Features include:

* custom target image
* free target zone positioning and sizing
* custom zone labels
* ability to show or hide zone borders
* custom text and background colors for items
* image items
* items prompting for additional (numerical) input after being dropped
* decoy items that don't have a zone
* feedback popups for both correct and incorrect attempts
* introductory and final feedback

The XBlock supports progressive grading and keeps progress across
refreshes. All checking and record keeping is done on the server side.

The following screenshot shows the Drag and Drop XBlock rendered
inside the edX LMS before the user starts solving the problem:

![Student view start](https://raw.githubusercontent.com/edx-solutions/xblock-drag-and-drop-v2/c955a38dc3a1aaf609c586d293ce19b282e11ffd/doc/img/student-view-start.png)

This screenshot shows the XBlock after the learner successfully
completed the Drag and Drop problem:

![Student view finish](https://raw.githubusercontent.com/edx-solutions/xblock-drag-and-drop-v2/c955a38dc3a1aaf609c586d293ce19b282e11ffd/doc/img/student-view-finish.png)

Installation
------------

Install the requirements into the Python virtual environment of your
`edx-platform` installation by running the following command from the
root folder:

```bash
$ pip install -r requirements.txt
```

Theming
-------

The Drag and Drop XBlock ships with an alternate theme called "Apros"
that you can enable by adding the following entry to `XBLOCK_SETTINGS`
in `lms.env.json`:

```json
        "drag-and-drop-v2": {
            "theme": {
                "package": "drag_and_drop_v2",
                "locations": ["public/themes/apros.css"]
            }
        }
```

You can use the same approach to apply a custom theme:

`"package"` can refer to any Python package in your virtualenv, which
means you can develop and maintain your own theme in a separate
package. There is no need to fork or modify this repository in any way
to customize the look and feel of your Drag and Drop problems.

`"locations"` is a list of relative paths pointing to CSS files
belonging to your theme. While the XBlock loads, files will be added
to it in the order that they appear in this list. (This means that if
there are rules with identical selectors spread out over different
files, rules in files that appear later in the list will take
precedence over those that appear earlier.)

Finally, note that the default (unthemed) appearance of the Drag and
Drop XBlock has been optimized for accessibility, so its use is
encouraged -- especially for courses targeting large and/or
potentially diverse audiences.

Enabling in Studio
------------------

You can enable the Drag and Drop XBlock in Studio through the Advanced
Settings.

1. From the main page of a specific course, navigate to `Settings ->
   Advanced Settings` from the top menu.
2. Check for the `Advanced Module List` policy key, and add
   `"drag-and-drop-v2"` to the policy value list.
3. Click the "Save changes" button.

Usage
-----

The Drag and Drop XBlock features an interactive editor. Add the Drag
and Drop component to a lesson, then click the `EDIT` button.

![Edit view](https://raw.githubusercontent.com/edx-solutions/xblock-drag-and-drop-v2/c955a38dc3a1aaf609c586d293ce19b282e11ffd/doc/img/edit-view.png)

In the first step, you can set some basic properties of the component,
such as the title, the maximum score, the problem text to render
above the background image, the introductory feedback (shown
initially), and the final feedback (shown after the learner
successfully completes the drag and drop problem).

![Drop zone edit](https://raw.githubusercontent.com/edx-solutions/xblock-drag-and-drop-v2/c955a38dc3a1aaf609c586d293ce19b282e11ffd/doc/img/edit-view-zones.png)

In the next step, you set the URL and description for the background
image and define the properties of the drop zones. For each zone you
can specify the text that should be rendered inside it (the "zone
label"), how wide and tall it should be, and where it should be placed
on the background image. In this step you can also specify whether you
would like zone labels to be shown to learners or not, as well as
whether or not to display borders outlining the zones. It is possible
to define an arbitrary number of drop zones as long as their labels
are unique.

![Drag item edit](https://raw.githubusercontent.com/edx-solutions/xblock-drag-and-drop-v2/c955a38dc3a1aaf609c586d293ce19b282e11ffd/doc/img/edit-view-items.png)

In the final step, you define the background and text color for drag
items, as well as the drag items themselves. A drag item can contain
either text or an image. You can define custom success and error
feedback for each item. The feedback text is displayed in a popup
after the learner drops the item on a zone - the success feedback is
shown if the item is dropped on the correct zone, while the error
feedback is shown when dropping the item on an incorrect drop zone.

Additionally, items can have a numerical value (and an optional error
margin) associated with them. When a learner drops an item that has a
numerical value on the correct zone, an input field for entering a
value is shown next to the item. The value that the learner submits is
checked against the expected value for the item. If you also specify a
margin, the value entered by the learner will be considered correct if
it does not differ from the expected value by more than that margin
(and incorrect otherwise).

![Zone dropdown](https://raw.githubusercontent.com/edx-solutions/xblock-drag-and-drop-v2/c955a38dc3a1aaf609c586d293ce19b282e11ffd/doc/img/edit-view-zone-dropdown.png)

The zone that an item belongs to is selected from a dropdown that
includes all drop zones defined in the previous step and a `none`
option that can be used for "decoy" items - items that don't belong to
any zone.

You can define an arbitrary number of drag items.

Analytics Events
----------------

The following analytics events are provided by this block.

## `edx.drag_and_drop_v2.loaded`

Fired when the Drag and Drop XBlock is finished loading.

Example ("common" fields that are not interesting in this context have been left out):

```
{
...
    "event": {},
    "event_source": "server",                              --  Common field, contains event source.
    "event_type": "edx.drag_and_drop_v2.loaded",           --  Common field, contains event name.
...
```

Real event example (taken from a devstack):
```
{
    "username": "staff",
    "event_type": "edx.drag_and_drop_v2.loaded",
    "ip": "10.0.2.2",
    "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0",
    "host": "precise64",
    "referer": "http://example.com/courses/course-v1:DnD+DnD+DnD/courseware/ec546c58d2f447b7a9223c57b5de7344/756071f8de7f47c3b0ae726586ebbe16/1?activate_block_id=block-v1%3ADnD%2BDnD%2BDnD%2Btype%40vertical%2Bblock%40d2fc47476ca14c55816c4a1264a27280",
    "accept_language": "en;q=1.0, en;q=0.5",
    "event": {},
    "event_source": "server",
    "context": {
        "course_user_tags": {},
        "user_id": 5,
        "org_id": "DnD",
        "module": {
            "usage_key": "block-v1:DnD+DnD+DnD+type@drag-and-drop-v2+block@6b80ce1e8b78426898b47a834d72ffd3",
            "display_name": "Drag and Drop"
        },
        "course_id": "course-v1:DnD+DnD+DnD",
        "path": "/courses/course-v1:DnD+DnD+DnD/xblock/block-v1:DnD+DnD+DnD+type@drag-and-drop-v2+block@6b80ce1e8b78426898b47a834d72ffd3/handler/publish_event"
    },
    "time": "2016-01-13T01:52:41.330049+00:00",
    "page": "x_module"
}
```

## `edx.drag_and_drop_v2.item.picked_up`

Fired when a learner picks up a draggable item.

Example ("common" fields that are not interesting in this context have been left out):

```
{
...
    "event": {
      "item_id": 0,                                        --  ID of the draggable item.
    },
    "event_source": "server",                              --  Common field, contains event source.
    "event_type": "edx.drag_and_drop_v2.picked_up",        --  Common field, contains event name.
...
```

Real event example (taken from a devstack):

```
{
    "username": "staff",
    "event_type": "edx.drag_and_drop_v2.item.picked_up",
    "ip": "10.0.2.2",
    "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0",
    "host": "precise64",
    "referer": "http://example.com/courses/course-v1:DnD+DnD+DnD/courseware/ec546c58d2f447b7a9223c57b5de7344/756071f8de7f47c3b0ae726586ebbe16/1?activate_block_id=block-v1%3ADnD%2BDnD%2BDnD%2Btype%40vertical%2Bblock%40d2fc47476ca14c55816c4a1264a27280",
    "accept_language": "en;q=1.0, en;q=0.5",
    "event": {
        "item_id": 0,
    },
    "event_source": "server",
    "context": {
        "course_user_tags": {},
        "user_id": 5,
        "org_id": "DnD",
        "module": {
            "usage_key": "block-v1:DnD+DnD+DnD+type@drag-and-drop-v2+block@6b80ce1e8b78426898b47a834d72ffd3",
            "display_name": "Drag and Drop"
        },
        "course_id": "course-v1:DnD+DnD+DnD",
        "path": "/courses/course-v1:DnD+DnD+DnD/xblock/block-v1:DnD+DnD+DnD+type@drag-and-drop-v2+block@6b80ce1e8b78426898b47a834d72ffd3/handler/publish_event"
    },
    "time": "2016-01-13T01:58:44.395935+00:00",
    "page": "x_module"
}
```

## `edx.drag_and_drop_v2.item.dropped`

Fired when a learner drops a draggable item.

This event will be emitted when a learner drops a draggable item.

Example ("common" fields that are not interesting in this context have been left out):

```
{
...
    "event": {
      "input": null,
      "is_correct": true,                                  --  False if there is an input in the draggable item, and the learner provided the wrong answer. Otherwise true.
      "is_correct_location": true,                         --  Whether the draggable item has been placed in the correct location.
      "item_id": 0,                                        --  ID of the draggable item.
      "location": "The Top Zone",                          --  Name of the location the item was dragged to.
    },
    "event_source": "server",                              --  Common field, contains event source.
    "event_type": "edx.drag_and_drop_v2.dropped",          --  Common field, contains event name.
...
```

Real event example (taken from a devstack):

```
{
    "username": "staff",
    "event_type": "edx.drag_and_drop_v2.item.dropped",
    "ip": "10.0.2.2",
    "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0",
    "host": "precise64",
    "referer": "http://example.com/courses/course-v1:DnD+DnD+DnD/courseware/ec546c58d2f447b7a9223c57b5de7344/756071f8de7f47c3b0ae726586ebbe16/1?activate_block_id=block-v1%3ADnD%2BDnD%2BDnD%2Btype%40vertical%2Bblock%40d2fc47476ca14c55816c4a1264a27280",
    "accept_language": "en;q=1.0, en;q=0.5",
    "event": {
        "is_correct_location": true,
        "is_correct": true,
        "location": "The Top Zone",
        "item_id": 0,
        "input": null
    },
    "event_source": "server",
    "context": {
        "course_user_tags": {},
        "user_id": 5,
        "org_id": "DnD",
        "module": {
            "usage_key": "block-v1:DnD+DnD+DnD+type@drag-and-drop-v2+block@6b80ce1e8b78426898b47a834d72ffd3",
            "display_name": "Drag and Drop"
        },
        "course_id": "course-v1:DnD+DnD+DnD",
        "path": "/courses/course-v1:DnD+DnD+DnD/xblock/block-v1:DnD+DnD+DnD+type@drag-and-drop-v2+block@6b80ce1e8b78426898b47a834d72ffd3/handler/do_attempt"
    },
    "time": "2016-01-13T01:58:45.202313+00:00",
    "page": "x_module"
}
```

## `edx.drag_and_drop_v2.feedback.opened`

Fired when the feedback pop-up is opened.

Example ("common" fields that are not interesting in this context have been left out):

```
{
...
    "event": {
      "content": "Correct! This one belongs to The Top Zone.",  --  Content of the feedback popup.
      "truncated": false,                                       --  Boolean indicating whether "content" field was truncated.
    },
    "event_source": "server",                                   --  Common field, contains event source.
    "event_type": "edx.drag_and_drop_v2.feedback.opened",       --  Common field, contains event name.
...
```

Real event example (taken from a devstack):

```
{
    "username": "staff",
    "event_type": "edx.drag_and_drop_v2.feedback.opened",
    "ip": "10.0.2.2",
    "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0",
    "host": "precise64",
    "referer": "http://example.com/courses/course-v1:DnD+DnD+DnD/courseware/ec546c58d2f447b7a9223c57b5de7344/756071f8de7f47c3b0ae726586ebbe16/1?activate_block_id=block-v1%3ADnD%2BDnD%2BDnD%2Btype%40vertical%2Bblock%40d2fc47476ca14c55816c4a1264a27280",
    "accept_language": "en;q=1.0, en;q=0.5",
    "event": {
        "content": "Correct! This one belongs to The Top Zone.",
        "truncated": false,
    },
    "event_source": "server",
    "context": {
        "course_user_tags": {},
        "user_id": 5,
        "org_id": "DnD",
        "module": {
            "usage_key": "block-v1:DnD+DnD+DnD+type@drag-and-drop-v2+block@6b80ce1e8b78426898b47a834d72ffd3",
            "display_name": "Drag and Drop"
        },
        "course_id": "course-v1:DnD+DnD+DnD",
        "path": "/courses/course-v1:DnD+DnD+DnD/xblock/block-v1:DnD+DnD+DnD+type@drag-and-drop-v2+block@6b80ce1e8b78426898b47a834d72ffd3/handler/publish_event"
    },
    "time": "2016-01-13T01:58:45.844986+00:00",
    "page": "x_module"
}
```

## `edx.drag_and_drop_v2.feedback.closed`

Fired when the feedback popup is closed.

Example ("common" fields that are not interesting in this context have been left out):

```
{
...
    "event": {
      "content": "No, this item does not belong here. Try again." --  Message of the feedback popup that was closed.
      "manually": true,                                           --  Whether or not the user closed the feedback window manually or if it was auto-closed.
      "truncated": false,                                         --  Boolean indicating whether "content" field was truncated.
    },
    "event_source": "server",                                     --  Common field, contains event source.
    "event_type": "edx.drag_and_drop_v2.feedback.closed",         --  Common field, contains event name.
...
```

Real event example (taken from a devstack):

```
{
    "username": "staff",
    "event_type": "edx.drag_and_drop_v2.feedback.closed",
    "ip": "10.0.2.2",
    "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0",
    "host": "precise64",
    "referer": "http://example.com/courses/course-v1:DnD+DnD+DnD/courseware/ec546c58d2f447b7a9223c57b5de7344/756071f8de7f47c3b0ae726586ebbe16/1?activate_block_id=block-v1%3ADnD%2BDnD%2BDnD%2Btype%40vertical%2Bblock%40d2fc47476ca14c55816c4a1264a27280",
    "accept_language": "en;q=1.0, en;q=0.5",
    "event": {
        "content": "No, this item does not belong here. Try again."
        "manually": true
        "truncated": false,
    },
    "event_source": "server",
    "context": {
        "course_user_tags": {},
        "user_id": 5,
        "org_id": "DnD",
        "module": {
            "usage_key": "block-v1:DnD+DnD+DnD+type@drag-and-drop-v2+block@13d1b859a2304c858e1810ccc23f29b2",
            "display_name": "Drag and Drop"
        },
        "course_id": "course-v1:DnD+DnD+DnD",
        "path": "/courses/course-v1:DnD+DnD+DnD/xblock/block-v1:DnD+DnD+DnD+type@drag-and-drop-v2+block@13d1b859a2304c858e1810ccc23f29b2/handler/publish_event"
    },
    "time": "2016-01-13T02:07:00.988534+00:00",
    "page": "x_module"
}
```


Testing
-------

Inside a fresh virtualenv, `cd` into the root folder of this repository
(`xblock-drag-and-drop-v2`) and run

```bash
$ sh install_test_deps.sh
```

You can then run the entire test suite via

```bash
$ python run_tests.py
```

To only run the unit test suite, do

```bash
$ python run_tests.py tests/unit/
```

Similarly, you can run the integration test suite via

```bash
$ python run_tests.py tests/integration/
```
