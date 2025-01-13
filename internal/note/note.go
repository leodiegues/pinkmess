package note

import (
	"log"
	"os"
	"time"
)

// A note representation
type Note struct {
	// Path to the note
	path string
}

// Creates a new note from a path.
func New(path string) *Note {
	return &Note{path: path}
}

// Creates a new empty note with it's corresponding file.
func (n *Note) NewEmpty() *Note {
	fileName := time.Now().Format("%Y%m%d%H%M%S")

	file, err := os.Create(fileName)
	if err != nil {
		log.Fatal(err)
	}

	defer file.Close()

	return New(fileName)
}
