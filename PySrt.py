import re
import sys

class SrtSection:
    """
        This class is used to stock a section from a srt file (subtitle frames).
        - self.beginning is the time (in seconds) where the subframe begins
        - self.duration is the duration (in seconds) of the subframe
        - self.content is the content of the subframe
    """

    def __init__(self, beginning, duration, content):
        self.beginning = beginning
        self.duration = duration
        self.content = content


    def __repr__(self):
        return '({0}, {1}), "{2}"'.format(self.beginning, self.duration, self.content.encode("unicode_escape").decode())


    def export(self):
        """
            Exports the section to a formatted string
        """

        return self.__export_tdata() + '\n' + self.content


    def __export_tdata(self):
        """
            Writes the time section in the srt syntax from the tuple
            (beginning, duration)
        """

        # Calculates each momentum
        beginning, end = self.beginning, self.beginning + self.duration 
        
        times = []
        for temps in beginning, end:
            hours = int(temps // 3600)
            temps %= 3600
            minutes = int(temps // 60)
            temps %= 60
            seconds = int(temps)
            miliseconds = int(round(temps - seconds, 3)*1000)

            times.append('{0}:{1}:{2},{3}'.format(hours, minutes, seconds, 
                                                  miliseconds))

        return ' --> '.join(times)



class SrtSubs:
    """ 
        This class is used to stock and manipulate sections from a srt file.

        self.sections, where all the datas are stored, is a list of SrtSections.
    """

    def __init__(self, string):
        """
            string is the content of the srt file.
        """

        self.rawsections = [s.strip() for s in string.split("\n\n") if s != '']
        self.sections = self.__extract_sections()


    def __extract_sections(self):
        """
            Extracts all the informations from a list containing all the
        sections of the file, in the form of a list of tuples :
        ((beginning, duration), content)
        with
            beginning and duration in seconds
            content the sub to show at this time
        """
        
        sections = []
        
        for section in self.rawsections:
            lines = section.split('\n')
            beginning, duration = self.__extract_tdata(lines[1])
            content = "\n".join(lines[2:])
            sections.append(SrtSection(beginning, duration, content))

        return sections


    def export_sections(self):
        """
            Writes the sections to a string to be written to the subs file
        """

        secs = []
        for number, section in enumerate(self.sections):
            sec = str(number+1)+'\n'
            sec += section.export()
            secs.append(sec)

        return '\n\n'.join(secs)


    def __extract_tdata(self, timesection):
        """
            Returns a tuple (beginning, duration) from
            the %H:%M:%S --> %H:%M:%S line.
        """

        tparts = timesection.split(" --> ")

        beginning_end = []
        for sec in tparts:
            hours, minutes, seconds, miliseconds = tuple(map(int, re.split("[:,]", sec)))
            beginning_end.append(3600 * hours + 60 * minutes + seconds + miliseconds/1000)

        beginning, end = tuple(beginning_end)
        duration = end - beginning

        return beginning, round(duration)


