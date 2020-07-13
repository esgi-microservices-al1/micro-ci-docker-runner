import csv
import os


class StatusService:
    image_container_ids = []
    inUse = False

    def __init__(self, filename):
        print("init status service")
        self.filename = filename
        open('/opt/project/main/resources/' + self.filename, 'w').close()

    def readAllFiles(self):
        all_array = []
        for file in os.listdir("/opt/project/main/resources"):
            if file.endswith(".csv"):
                for img_container_ids in self.read(file):
                    all_array.append(img_container_ids)
        return all_array
    def read(self, filename):
        image_container_ids_array = []
        with open('/opt/project/main/resources/'+filename, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            for row in csv_reader:
                if row[0] and row[1]:
                    print(f'\t{row[0]},{row[1]}.')
                    image_container_ids_array.append((row[0], row[1], row[2], row[3]))
                    line_count += 1
            print(f'Processed {line_count} lines.')
            csv_file.close()
        return image_container_ids_array

    def write(self):
        with open('/opt/project/main/resources/'+self.filename, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for image_container_id in StatusService.image_container_ids:
                csv_writer.writerow(
                    [image_container_id[0], image_container_id[1], image_container_id[2], image_container_id[3]])
            csv_file.close()

    def add_image_ids(self, image_id, container_id, project_id, date_created):
        StatusService.image_container_ids = self.read(self.filename)
        StatusService.image_container_ids.append((image_id, container_id, project_id, str(date_created)))
        self.write()

    def delete_by_image_id(self, container_id):
        StatusService.image_container_ids = self.read(self.filename)
        for image_container_id in StatusService.image_container_ids:
            if image_container_id[0] == container_id:
                StatusService.image_container_ids.remove(image_container_id)
        self.write()
        os.remove('/opt/project/main/resources/'+self.filename)

    def checkIfOtherImage(self, image_id):
        count = 0
        all_array = self.readAllFiles()
        for image_container_id in all_array:
            if image_id == image_container_id[0]:
                count += 1
        return count
