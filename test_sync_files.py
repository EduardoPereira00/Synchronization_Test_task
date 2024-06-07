from sync_files import snapshot_source_folder, sync_new_files, sync_updated_files, sync_deleted_files
import pytest

# Sync new files -> test if the new file in the replica exists
# Sync updated files -> test if the file in the replica folder is updated
# Sync deleted files -> test if the file was deleted from the replica

@pytest.fixture
def setup_directories(tmp_path):
    source_dir = tmp_path / "source"
    replica_dir = tmp_path / "replica"
    source_dir.mkdir()
    replica_dir.mkdir()
    return source_dir, replica_dir


def test_sync_new_files(setup_directories):
    source, replica = setup_directories

    new_file = source / "new_file.txt"
    new_file.write_text("Test")

    snapshot = snapshot_source_folder(source)
    sync_new_files(snapshot, source, replica)

    assert(replica / "new_file.txt").exists()
    assert(replica / "new_file.txt").read_text() == "Test"



def test_sync_updated_files(setup_directories):
    source, replica = setup_directories

    file = source / "File_To_Update.txt"
    file.write_text("Update Test")
    snapshot = snapshot_source_folder(source)
    sync_new_files(snapshot, source, replica)

    file.write_text("Text Updated Test")
    snapshot = snapshot_source_folder(source)
    sync_updated_files(snapshot, source, replica)

    replica = replica / "File_To_Update.txt"

    assert replica.exists()
    assert replica.read_text() == "Text Updated Test"
    
def test_sync_deleted_files(setup_directories):
    source, replica = setup_directories

    file = replica / "File_To_Delete.txt"
    file.write_text("File to delete")

    assert replica.exists()

    snapshot = snapshot_source_folder(source)
    sync_deleted_files(snapshot, replica)

    assert not file.exists()