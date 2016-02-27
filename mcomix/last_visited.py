from mcomix import constants
import os

class _ArchiveEntry:
    def __init__(self, last_read, max, name):
        self._last_page = int(last_read);
        self._max = int(max);
        self._name = name.strip();

    def str(self):
        return "{}\t{}\t{}\n".format(self._last_page, self._max, self._name)

    def pretty(self):
        return "{} of {} in {}".format(self._read, self._max, self._name)

    def set_page(self, page):
        self._last_page = page

    def set_max(self, page):
        self._max = page

class LastVisited:

    """
    Saves the last position of all visited achives in a file.
    (~/.comixlast)
    """

    def __init__(self):
        # TODO Use `import preferences`?
        self.savefile = os.path.join(constants.HOME_DIR,
                                     ".comixlast")

        # Create the file if it doesn't exist, otherwise open it.
        if not os.path.isfile(self.savefile):
            self._savefile = open(self.savefile, "w+")
        else:
            self._savefile = open(self.savefile, "r+")

        # Read the file into a list
        self._archives = []
        self._archives = self._read_file(self._savefile)
        self._current_entry = False;

    def save_file(self):
        """
        Write the updated file to disk.
        """
        self._savefile.close()
        self._savefile = open(self.savefile, "w+")
        for line in self._archives:
            self._savefile.write(line.str())

    def update_entry(self, filehandler, imagehandler):
        """
        Either sets a new current entry or updates it
        """
        pathname = filehandler.get_path_to_base()
        if self._current_entry == False or self._current_entry._name != pathname:
            self._current_entry = self._find_entry(pathname)

        new_page = imagehandler.get_current_page()
        if self._current_entry._last_page < new_page:
            self._current_entry.set_page(new_page)

        self._current_entry.set_max(imagehandler.get_number_of_pages())

    def _find_entry(self, name):
        """
        Find an entry loaded from the savefile or create a new one and append
        it to the list
        """
        for e in self._archives:
            if name == e._name:
                return e
        e = _ArchiveEntry("0", "0", name)
        self._archives.append(e)
        return e

    def _read_file(self, _file):
        """
        Reads the whole file with items and returns a list of _ArchiveEntries
        """
        ret = []
        for line in _file:
            try:
                e = line.split("\t")
                ret.append(_ArchiveEntry(e[0], e[1], e[2]))
            except (IndexError, ValueError):
                print "Failed to load line:", line,

        return ret
